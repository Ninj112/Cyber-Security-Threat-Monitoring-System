from flask import Flask, render_template, request, jsonify
import json, time, os
from structures.threat_queue import ThreatQueue, Threat
from utils.loader import load_threats

app = Flask(__name__)

# Configuration
LOG_FILE = "data/attack_log.json"
BLOCKED_FILE = "data/blocked_ips.json"
THRESHOLD = 3

# Data structures
threat_map = load_threats("data/threats.txt")
queue = ThreatQueue()
seen = set()
blocked_ips = set()
attack_counts = {}
messages = []


def ensure_data_files():
    os.makedirs("data", exist_ok=True)
    for file in [LOG_FILE, BLOCKED_FILE]:
        if not os.path.exists(file):
            with open(file, "w") as f:
                json.dump([], f)


def save_blocked_ips():
    with open(BLOCKED_FILE, "w") as f:
        json.dump(list(blocked_ips), f, indent=2)


def load_new_attacks():
    try:
        with open(LOG_FILE, "r") as f:
            attacks = json.load(f)
    except:
        return

    for a in attacks:
        key = (a["ip"], a["time"])
        if key not in seen:
            seen.add(key)
            queue.push(Threat(a["ip"], a["attack"], a["severity"], a["time"]))
            
            ip = a["ip"]
            attack_counts[ip] = attack_counts.get(ip, 0) + 1

            if attack_counts[ip] >= THRESHOLD and ip not in blocked_ips:
                blocked_ips.add(ip)
                save_blocked_ips()
                messages.append(f"[AUTO-BLOCK] IP {ip} blocked after {attack_counts[ip]} attacks")


# Initialize
ensure_data_files()
try:
    with open(BLOCKED_FILE) as f:
        blocked_ips.update(json.load(f))
except:
    pass


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
    """Handle attack requests from the attacker console."""
    data = request.json
    ip = data.get('ip', '').strip()
    attack_type = data.get('attack', '').strip()

    ip = request.json.get('ip', '').strip()
    attack_type = request.json.get('attack', '').strip()

    if not ip or not attack_type:
        return jsonify({"status": "error", "message": "IP and attack type required"})
    
    if attack_type not in threat_map:
        return jsonify({"status": "error", "message": f"Unknown attack: {attack_type}"})
    
    if ip in blocked_ips:
        return jsonify({"status": "blocked", "message": f"IP {ip} is blocked"})

    entry = {"ip": ip, "attack": attack_type, "severity": threat_map[attack_type], "time": time.time()}
    
    try:
        with open(LOG_FILE, "r") as f:
            log_data = json.load(f)
    except:
        log_data = []
    
    log_data.append(entry)
    
    with open(LOG_FILE, "w") as f:
        json.dump(log_data, f, indent=2)

    return jsonify({"status": "success", "severity": entry["severity"]"""Get all current threats."""
    load_new_attacks()
    threats_list = []
    for threat in queue.all():
        threats_list.append({
            "ip": threat.ip,
            "attack": threat.attack,
            "severity": threat.severity,
            "time": threat.time,
            "blocked": threat.ip in blocked_ips
        })
    
    return jsonify({
        "threats": threats_list,
        "messages": messages[-10:],  # Last 10 messages
        "blocked_count": len(blocked_ips)
    })


@app.route('/defender_command', methods=['POST'])
def defender_command():
    """Handle commands from the defender console."""
    data = request.json
    cmd = data.get('command', '').strip().lower()
    response = {"output": "", "show_table": False, "threats": []}

    if cmd == "view":
        load_new_attacks()
        response["show_table"] = True
        response["threats"] = [{"status": "Blocked" if t.ip in blocked_ips else "Active", "severity": t.severity, "ip": t.ip, "attack": t.attack, "time": time.ctime(t.time)} for t in queue.all()]ATE] {ip} isolated by defender")
            
    elif cmd.startswith("alert "):
        # Send alert message
        message = cmd.split(" ", 1)[1].strip()
        messages.append(f"[ADMIN-ALERT] {message}")
        response["output"] = f"✓ Alert sent to security team:\n  '{message}'"
        
    elif cmd.startswith("block "):
        # Block an IP address
        ip = cmd.split(" ", 1)[1].strip()
        if ip in blocked_ips:
            response["output"] = f"IP {ip} is already blocked"
        else:
        ip = cmd.split(" ", 1)[1].strip()
        if ip in blocked_ips:
            response["output"] = f"IP {ip} is already isolated"
        else:
            blocked_ips.add(ip)
            save_blocked_ips()
            response["output"] = f"✓ IP {ip} isolated"
            
    elif cmd.startswith("alert "):
        messages.append(f"[ALERT] {cmd.split(' ', 1)[1].strip()}")
        response["output"] = "✓ Alert sent"
        
    elif cmd.startswith("block "):
        ip = cmd.split(" ", 1)[1].strip()
        if ip in blocked_ips:
            response["output"] = f"IP {ip} already blocked"
        else:
            blocked_ips.add(ip)
            save_blocked_ips()
            response["output"] = f"✓ IP {ip} blocked"
            
    elif cmd.startswith("unblock "):
        ip = cmd.split(" ", 1)[1].strip()
        if ip not in blocked_ips:
            response["output"] = f"IP {ip} not blocked"
        else:
            blocked_ips.remove(ip)
            save_blocked_ips()
            attack_counts[ip] = 0
        load_new_attacks()
        counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
        for t in queue.all():
            counts[t.severity] += 1
        response["output"] = f"=== STATISTICS ===\nTotal: {queue.size()}\nBlocked: {len(blocked_ips)}\nHIGH: {counts['HIGH']} | MEDIUM: {counts['MEDIUM']} | LOW: {counts['LOW']}"
        
    elif cmd == "blocked":
        response["output"] = "=== BLOCKED IPs ===\n" + "\n".join(f"  • {ip}" for ip in sorted(blocked_ips)) if blocked_ips else "No blocked IPs"
            
    elif cmd == "clear":
        messages.clear()
        response["output"] = "✓ C

@app.route('/status')
def status():
    """Get system status."""
    load_new_attacks()
    return jsonify({
        "total_threats": queue.size(),
        "blocked_ips": len(blocked_ips),
        "messages_count": len(messages),
        response["output"] = "Commands: view | stats | blocked | isolate <ip> | block <ip> | unblock <ip> | alert <msg> | clear"
    else:
        response["output"] = f"Unknown: '{cmd}' | Type 'help'"

    return jsonify(response)


@app.route('/status')
def status():
    load_new_attacks()
    return jsonify({"total_threats": queue.size(), "blocked_ips": len(blocked_ips), "messages": len(messages), "attack_types": len(threat_map)})


if __name__ == '__main__':
    print(f"Starting... {len(threat_map)} attack types loaded, threshold={THRESHOLD}")
    app.run(debug=True