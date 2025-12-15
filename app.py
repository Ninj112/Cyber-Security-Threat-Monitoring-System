"""
Cyber Security Threat Monitoring System - Main Application
A Flask-based web application for simulating and monitoring cyber threats
"""
from flask import Flask, render_template, request, jsonify
import json
import time
import os
from structures.threat_queue import ThreatQueue, Threat
from structures.linked_list import ThreatLinkedList
from structures.threat_graph import ThreatGraph
from utils.loader import load_threats

app = Flask(__name__)

# Configuration
LOG_FILE = "data/attack_log.json"
THREAT_FILE = "data/threats.txt"
BLOCKED_FILE = "data/blocked_ips.json"
THRESHOLD = 3  # Number of attacks before auto-blocking

# Initialize data structures
threat_map = load_threats(THREAT_FILE)
queue = ThreatQueue()              # Priority Queue for threat ranking
threat_history = ThreatLinkedList()  # Linked List for dynamic logging
threat_graph = ThreatGraph()       # Graph for pattern recognition
seen = set()                       # Hash Set for duplicate detection
blocked_ips = set()                # Hash Set for blocked IPs
attack_counts = {}                 # Hash Map for attack counting
messages = []


def ensure_data_files():
    """Ensure all data files and directories exist."""
    os.makedirs("data", exist_ok=True)
    
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            json.dump([], f)
    
    if not os.path.exists(BLOCKED_FILE):
        with open(BLOCKED_FILE, "w") as f:
            json.dump([], f)


def load_blocked_ips():
    """Load blocked IPs from file."""
    try:
        with open(BLOCKED_FILE, "r") as f:
            data = json.load(f)
            blocked_ips.update(data)
            print(f"Loaded {len(blocked_ips)} blocked IPs")
    except FileNotFoundError:
        print("No blocked IPs file found, starting fresh")
    except Exception as e:
        print(f"Error loading blocked IPs: {e}")


def save_blocked_ips():
    """Save blocked IPs to file."""
    try:
        with open(BLOCKED_FILE, "w") as f:
            json.dump(list(blocked_ips), f, indent=2)
    except Exception as e:
        print(f"Error saving blocked IPs: {e}")


def load_new_attacks():
    """Load new attacks from the log file and add them to the queue."""
    try:
        with open(LOG_FILE, "r") as f:
            attacks = json.load(f)
    except FileNotFoundError:
        return
    except Exception as e:
        print(f"Error loading attacks: {e}")
        return

    for attack_data in attacks:
        key = (attack_data["ip"], attack_data["time"])
        if key not in seen:
            seen.add(key)
            threat = Threat(
                ip=attack_data["ip"],
                attack=attack_data["attack"],
                severity=attack_data["severity"],
                time=attack_data["time"]
            )
            queue.push(threat)

            # Count attacks per IP
            ip = attack_data["ip"]
            attack_counts[ip] = attack_counts.get(ip, 0) + 1

            # Auto-block after threshold
            if attack_counts[ip] >= THRESHOLD and ip not in blocked_ips:
                blocked_ips.add(ip)
                save_blocked_ips()
                messages.append(f"[AUTO-BLOCK] IP {ip} blocked after {attack_counts[ip]} attacks")
                messages.append(f"[ISOLATED] Device {ip} has been isolated from the network")
                messages.append(f"[ALERT] Security admin notified about IP {ip}")
            
            # Build graph connections for pattern recognition
            if attack_counts[ip] > 1:
                for other_ip in attack_counts:
                    if other_ip != ip and attack_counts[other_ip] > 1:
                        threat_graph.add_connection(ip, other_ip)


# Initialize on startup
ensure_data_files()
load_blocked_ips()


@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')


@app.route('/attacker')
def attacker():
    """Render the attacker console."""
    return render_template('attacker.html')


@app.route('/defender')
def defender():
    """Render the defender console."""
    return render_template('defender.html')


@app.route('/attack', methods=['POST'])
def attack():
    """Handle attack requests from the attacker console."""
    data = request.json
    ip = data.get('ip', '').strip()
    attack_type = data.get('attack', '').strip()

    # Validation
    if not ip or not attack_type:
        return jsonify({
            "status": "error",
            "message": "IP address and attack type are required"
        })

    # Check if attack type is known
    if attack_type not in threat_map:
        return jsonify({
            "status": "error",
            "message": f"Unknown attack type: {attack_type}"
        })

    # Check if IP is blocked
    if ip in blocked_ips:
        return jsonify({
            "status": "blocked",
            "message": f"IP {ip} is currently blocked and cannot execute attacks"
        })

    # Create attack entry
    severity = threat_map[attack_type]
    entry = {
        "ip": ip,
        "attack": attack_type,
        "severity": severity,
        "time": time.time()
    }

    # Save to log file
    try:
        with open(LOG_FILE, "r") as f:
            log_data = json.load(f)
    except:
        log_data = []

    log_data.append(entry)
    
    # Add to linked list for dynamic logging
    threat_history.add(entry)

    try:
        with open(LOG_FILE, "w") as f:
            json.dump(log_data, f, indent=2)
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to log attack: {str(e)}"
        })

    return jsonify({
        "status": "success",
        "message": f"Attack '{attack_type}' from {ip} logged successfully",
        "severity": severity
    })


@app.route('/threats')
def threats():
    """Get all current threats."""
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
        # Load latest attacks and display them
        load_new_attacks()
        threats_list = []
        for threat in queue.all():
            status = "Blocked" if threat.ip in blocked_ips else "Active"
            threats_list.append({
                "status": status,
                "severity": threat.severity,
                "ip": threat.ip,
                "attack": threat.attack,
                "time": time.ctime(threat.time)
            })
        response["show_table"] = True
        response["threats"] = threats_list
        
    elif cmd.startswith("isolate "):
        # Isolate an IP address
        ip = cmd.split(" ", 1)[1].strip()
        if ip in blocked_ips:
            response["output"] = f"IP {ip} is already isolated"
        else:
            blocked_ips.add(ip)
            save_blocked_ips()
            response["output"] = f"✓ IP {ip} has been isolated\n✓ Device removed from network\n✓ Admin notification sent"
            messages.append(f"[MANUAL-ISOLATE] {ip} isolated by defender")
            
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
            blocked_ips.add(ip)
            save_blocked_ips()
            response["output"] = f"✓ IP {ip} has been blocked"
            messages.append(f"[MANUAL-BLOCK] {ip} blocked by defender")
            
    elif cmd.startswith("unblock "):
        # Unblock an IP address
        ip = cmd.split(" ", 1)[1].strip()
        if ip not in blocked_ips:
            response["output"] = f"IP {ip} is not currently blocked"
        else:
            blocked_ips.remove(ip)
            save_blocked_ips()
            attack_counts[ip] = 0  # Reset count
            response["output"] = f"✓ IP {ip} has been unblocked"
            messages.append(f"[UNBLOCK] {ip} unblocked by defender")
            
    elif cmd == "stats":
        # Show statistics
        load_new_attacks()
        severity_counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
        for threat in queue.all():
            severity_counts[threat.severity] = severity_counts.get(threat.severity, 0) + 1
        
        stats_output = f"""=== THREAT STATISTICS ===
Total Threats: {queue.size()}
Blocked IPs: {len(blocked_ips)}

Severity Breakdown:
  HIGH:   {severity_counts['HIGH']} threats
  MEDIUM: {severity_counts['MEDIUM']} threats
  LOW:    {severity_counts['LOW']} threats

Recent Activity: {len(messages)} events logged
"""
        response["output"] = stats_output
        
    elif cmd == "blocked":
        # List all blocked IPs
        if blocked_ips:
            response["output"] = "=== BLOCKED IPs ===\n" + "\n".join(f"  • {ip}" for ip in sorted(blocked_ips))
        else:
            response["output"] = "No IPs are currently blocked"
            
    elif cmd == "clear":
        # Clear message log
        messages.clear()
        response["output"] = "✓ Message log cleared"
        
    elif cmd.startswith("recent"):
        # Show recent attacks from linked list
        parts = cmd.split()
        n = int(parts[1]) if len(parts) > 1 else 10
        recent = threat_history.get_recent(n)
        if recent:
            response["output"] = "=== RECENT ATTACKS ===\n" + "\n".join([
                f"  {i+1}. {a['attack']} from {a['ip']} [{a['severity']}]"
                for i, a in enumerate(recent)
            ])
        else:
            response["output"] = "No recent attacks found"
    
    elif cmd == "patterns":
        # Show attack patterns from graph
        patterns = threat_graph.find_patterns()
        if patterns:
            response["output"] = "=== ATTACK PATTERNS ===\n"
            for i, cluster in enumerate(patterns, 1):
                response["output"] += f"\nPattern {i}: {', '.join(cluster)}"
        else:
            response["output"] = "No attack patterns detected yet"
    
    elif cmd.startswith("related "):
        # Show related IPs from graph
        ip = cmd.split(" ", 1)[1].strip()
        related = threat_graph.get_related(ip)
        if related:
            response["output"] = f"=== IPs RELATED TO {ip} ===\n" + "\n".join(f"  • {r}" for r in related)
        else:
            response["output"] = f"No related IPs found for {ip}"
    
    elif cmd == "help":
        # Show help
        response["output"] = """=== DEFENDER COMMANDS ===
  view              - View all current threats in table
  stats             - Show threat statistics
  blocked           - List all blocked IPs
  recent [n]        - Show n recent attacks (default 10)
  patterns          - Show attack patterns (graph analysis)
  related <ip>      - Show IPs with similar attack patterns
  isolate <ip>      - Isolate a device from network
  block <ip>        - Block an IP address
  unblock <ip>      - Unblock an IP address
  alert <message>   - Send alert to security team
  clear             - Clear message log
  help              - Show this help message
"""
    else:
        response["output"] = f"Unknown command: '{cmd}'\nType 'help' for available commands"

    return jsonify(response)


@app.route('/status')
def status():
    """Get system status."""
    load_new_attacks()
    return jsonify({
        "total_threats": queue.size(),
        "blocked_ips": len(blocked_ips),
        "messages_count": len(messages),
        "attack_types": len(threat_map)
    })


if __name__ == '__main__':
    print("Starting Cyber Security Threat Monitoring System...")
    print(f"Loaded {len(threat_map)} attack types")
    print(f"Auto-block threshold: {THRESHOLD} attacks")
    app.run(debug=True, host='127.0.0.1', port=5000)