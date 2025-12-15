from flask import Flask, render_template, request, jsonify
import json
import time
from structures.threat_queue import ThreatQueue, Threat
from structures.linked_list import ThreatLinkedList
from utils.loader import load_threats

app = Flask(__name__)

LOG_FILE = "data/attack_log.json"
THREAT_FILE = "data/threats.txt"
BLOCKED_FILE = "data/blocked_ips.json"

threat_map = load_threats(THREAT_FILE)
queue = ThreatQueue()
seen = set()
blocked_ips = set()
attack_counts = {}
messages = []

THRESHOLD = 3  # Number of attacks before blocking

def load_blocked_ips():
    try:
        with open(BLOCKED_FILE) as f:
            data = json.load(f)
            blocked_ips.update(data)
    except:
        pass

def save_blocked_ips():
    with open(BLOCKED_FILE, "w") as f:
        json.dump(list(blocked_ips), f)

def load_new_attacks():
    try:
        with open(LOG_FILE) as f:
            attacks = json.load(f)
    except:
        return

    for a in attacks:
        key = (a["ip"], a["time"])
        if key not in seen:
            seen.add(key)
            threat = Threat(**a)
            queue.push(threat)

            # Count attacks per IP
            ip = a["ip"]
            if ip not in attack_counts:
                attack_counts[ip] = 0
            attack_counts[ip] += 1

            # Check if should block
            if attack_counts[ip] >= THRESHOLD and ip not in blocked_ips:
                blocked_ips.add(ip)
                save_blocked_ips()
                messages.append(f"[BLOCKED] IP {ip} has been blocked due to multiple attacks.")
                messages.append(f"[ISOLATED] Device {ip} has been isolated.")
                messages.append(f"[ALERT] Admin alerted about suspicious activity from {ip}.")

load_blocked_ips()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/attacker')
def attacker():
    return render_template('attacker.html')

@app.route('/defender')
def defender():
    return render_template('defender.html')

@app.route('/attack', methods=['POST'])
def attack():
    data = request.json
    ip = data.get('ip')
    attack_type = data.get('attack')
    if ip and attack_type:
        if ip in blocked_ips:
            return jsonify({"status": "blocked", "message": f"IP {ip} is blocked."})

        entry = {
            "ip": ip,
            "attack": attack_type,
            "severity": threat_map.get(attack_type, "LOW"),
            "time": time.time()
        }

        try:
            with open(LOG_FILE, "r") as f:
                log_data = json.load(f)
        except:
            log_data = []

        log_data.append(entry)

        with open(LOG_FILE, "w") as f:
            json.dump(log_data, f, indent=2)

        return jsonify({"status": "success"})
    return jsonify({"status": "error"})

@app.route('/threats')
def threats():
    load_new_attacks()
    threats_list = []
    for t in queue.all():
        threats_list.append({
            "ip": t.ip,
            "attack": t.attack,
            "severity": t.severity
        })
    return jsonify({"threats": threats_list, "messages": messages})

@app.route('/defender_command', methods=['POST'])
def defender_command():
    data = request.json
    cmd = data.get('command', '').strip().lower()
    response = {"output": "", "show_table": False, "threats": []}

    if cmd == "view":
        load_new_attacks()
        threats_list = []
        for t in queue.all():
            status = "Blocked" if t.ip in blocked_ips else "Active"
            threats_list.append({
                "status": status,
                "severity": t.severity,
                "ip": t.ip,
                "attack": t.attack,
                "time": time.ctime(t.time)
            })
        response["show_table"] = True
        response["threats"] = threats_list
    elif cmd.startswith("isolate "):
        ip = cmd.split(" ", 1)[1]
        if ip in blocked_ips:
            response["output"] = f"IP {ip} is already isolated."
        else:
            blocked_ips.add(ip)
            save_blocked_ips()
            response["output"] = f"IP {ip} has been isolated. Admin alerted."
            messages.append(f"[ISOLATED] Device {ip} has been isolated.")
            messages.append(f"[ALERT] Admin alerted about suspicious activity from {ip}.")
    elif cmd.startswith("alert "):
        message = cmd.split(" ", 1)[1]
        messages.append(f"[ALERT] {message}")
        response["output"] = "Alert sent to admin."
    elif cmd.startswith("block "):
        ip = cmd.split(" ", 1)[1]
        if ip in blocked_ips:
            response["output"] = f"IP {ip} is already blocked."
        else:
            blocked_ips.add(ip)
            save_blocked_ips()
            response["output"] = f"IP {ip} has been blocked."
    elif cmd.startswith("unblock "):
        ip = cmd.split(" ", 1)[1]
        if ip not in blocked_ips:
            response["output"] = f"IP {ip} is not blocked."
        else:
            blocked_ips.remove(ip)
            save_blocked_ips()
            response["output"] = f"IP {ip} has been unblocked."
    elif cmd == "help":
        response["output"] = "Commands:\n  view       - View current threats\n  isolate <ip> - Isolate an IP and alert admin\n  alert <msg>  - Send alert message to admin\n  block <ip>   - Block an IP\n  unblock <ip> - Unblock an IP\n"
    else:
        response["output"] = "Unknown command. Type 'help' for available commands."

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)