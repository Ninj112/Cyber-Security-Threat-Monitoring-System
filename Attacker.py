import tkinter as tk
import time

class Attack:
    def __init__(self, ip, attack_type, timestamp):
        self.ip = ip
        self.attack_type = attack_type
        self.timestamp = timestamp

attacks = []

def is_valid_ip(ip):
    parts = ip.split(".")
    if len(parts) != 4:
        return False

    for part in parts:
        if not part.isdigit():
            return False
        num = int(part)
        if num < 0 or num > 255:
            return False

    return True

def submit_attack():
    ip = ip_entry.get()
    attack_type = type_var.get()

    if not is_valid_ip(ip):
        status_label.config(text="Invalid IP address")
        return

    if attack_type.strip() == "":
        status_label.config(text="Choose attack type")
        return

    attack = Attack(ip, attack_type, time.time())
    attacks.append(attack)

    update_listbox()
    clear_fields()
    status_label.config(text="Attack submitted")

def update_listbox():
    listbox.delete(0, tk.END)
    for a in attacks:
        listbox.insert(tk.END, f"{a.ip} | {a.attack_type}")

def clear_fields():
    ip_entry.delete(0, tk.END)
    type_var.set(" ")

# ---------- UI ----------

root = tk.Tk()
root.title("Attacker Panel")
root.geometry("400x400")

tk.Label(root, text="My IP").pack()
ip_entry = tk.Entry(root)
ip_entry.pack()

tk.Label(root, text="Attack Type").pack()
type_var = tk.StringVar(value=" ")
tk.OptionMenu(
    root,
    type_var,
    "DoS",
    "SQL Injection",
    "Remote Code Execution",
    "Privilege Escalation",
    "Ransomware Attempt",
    "Zero-Day Exploit",
    "Data Exfiltration",
    "Command Injection",
    "Brute Force Login",
    "DDoS Attempt",
    "Cross-Site Scripting (XSS)",
    "Malware Download",
    "Unauthorized API Access",
    "Credential Stuffing",
    "Suspicious File Upload",
    "Port Scan",
    "Ping Sweep",
    "Banner Grabbing",
    "Directory Enumeration",
    "Suspicious Login Attempt",
    "Unknown Traffic Pattern"
).pack()

tk.Button(root, text="Submit Attack", command=submit_attack).pack(pady=10)

status_label = tk.Label(root, text="")
status_label.pack()

tk.Label(root, text="Submitted Attacks").pack()
listbox = tk.Listbox(root, width=50)
listbox.pack(fill=tk.BOTH, expand=True)

root.mainloop()
