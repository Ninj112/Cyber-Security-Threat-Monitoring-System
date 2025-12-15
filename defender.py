import json, time, threading
from structures.threat_queue import ThreatQueue, Threat
from structures.linked_list import ThreatLinkedList

LOG_FILE = "data/attack_log.json"
BLOCKED_FILE = "data/blocked_ips.json"

queue = ThreatQueue()
history = ThreatLinkedList()
seen = set()
blocked_ips = set()

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
            history.add(threat)

def monitor_attacks():
    while True:
        load_new_attacks()
        time.sleep(5)  # Check every 5 seconds

def print_threats():
    print("\nCurrent Threats:")
    for t in queue.all():
        status = "[BLOCKED]" if t.ip in blocked_ips else ""
        print(f"{status}[{t.severity}] {t.ip} | {t.attack}")
    print()

def print_history():
    print("\nThreat History:")
    current = history.head
    while current:
        status = "[BLOCKED]" if current.data.ip in blocked_ips else ""
        print(f"{status}[{current.data.severity}] {current.data.ip} | {current.data.attack} | {time.ctime(current.data.time)}")
        current = current.next
    print()

def block_ip(ip):
    if ip in blocked_ips:
        print(f"IP {ip} is already blocked.")
    else:
        blocked_ips.add(ip)
        save_blocked_ips()
        print(f"IP {ip} has been blocked.")

def unblock_ip(ip):
    if ip in blocked_ips:
        blocked_ips.remove(ip)
        save_blocked_ips()
        print(f"IP {ip} has been unblocked.")
    else:
        print(f"IP {ip} is not blocked.")

def main():
    load_blocked_ips()
    load_new_attacks()
    
    # Start monitoring thread
    monitor_thread = threading.Thread(target=monitor_attacks, daemon=True)
    monitor_thread.start()
    
    print("> Defender Monitoring Console")
    print("> Type 'help' for commands.\n")

    while True:
        command = input("defender> ").strip().lower()

        if command == "view":
            print_threats()
        elif command == "history":
            print_history()
        elif command.startswith("block "):
            ip = command.split(" ", 1)[1]
            block_ip(ip)
        elif command.startswith("unblock "):
            ip = command.split(" ", 1)[1]
            unblock_ip(ip)
        elif command == "help":
            print("Commands:")
            print("  view     - View current threats")
            print("  history  - View threat history")
            print("  block <ip>   - Block an IP")
            print("  unblock <ip> - Unblock an IP")
            print("  exit     - Exit the console")
            print()
        elif command == "exit":
            print("Exiting...")
            break
        else:
            print("Unknown command. Type 'help' for available commands.")

if __name__ == "__main__":
    main()