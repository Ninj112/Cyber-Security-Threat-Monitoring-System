from flask import Flask, render_template, request, jsonify
import json
import time
from structures.threat_queue import ThreatQueue, Threat
from structures.linked_list import ThreatLinkedList
from utils.loader import load_threats

app = Flask(__name__)

LOG_FILE = "data/attack_log.json"
THREAT_FILE = "data/threats.txt"

threat_map = load_threats(THREAT_FILE)
queue = ThreatQueue()
history = ThreatLinkedList()
seen = set()

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
            history.add(threat)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/attack', methods=['POST'])
def attack():
    data = request.json
    ip = data.get('ip')
    attack_type = data.get('attack')
    if ip and attack_type:
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
    return jsonify(threats_list)

if __name__ == '__main__':
    app.run(debug=True)