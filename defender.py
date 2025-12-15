import json, time, tkinter as tk
from structures.threat_queue import ThreatQueue, Threat
from structures.linked_list import ThreatLinkedList

LOG_FILE = "data/attack_log.json"

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

def refresh():
    load_new_attacks()
    table.delete(*table.get_children())
    for t in queue.all():
        table.insert("", "end", values=(t.ip, t.attack, t.severity))
    root.after(1000, refresh)

# ---------- GUI ----------
root = tk.Tk()
root.title("DEFENDER TERMINAL")
root.geometry("800x450")
root.configure(bg="black")

FONT = ("Courier New", 11)
FG = "#00ff00"

terminal = tk.Text(
    root,
    bg="black",
    fg=FG,
    insertbackground=FG,
    font=FONT,
    state="disabled"
)
terminal.pack(fill=tk.BOTH, expand=True)

# ---------- Functions ----------
def write(text):
    terminal.config(state="normal")
    terminal.insert(tk.END, text + "\n")
    terminal.see(tk.END)
    terminal.config(state="disabled")

def load_attacks():
    try:
        with open(LOG_FILE) as f:
            attacks = json.load(f)
    except:
        return

    for a in attacks:
        key = (a["ip"], a["time"])
        if key not in seen:
            seen.add(key)
            threat = Threat(a["ip"], a["attack"], a["severity"], a["time"])
            queue.push(threat)
            history.add(threat)
            write(f"[{threat.severity}] {threat.ip} | {threat.attack}")

def refresh():
    load_attacks()
    root.after(1000, refresh)

# ---------- Boot ----------
write("> Defender Monitoring Console")
write("> Waiting for threats...\n")

refresh()
root.mainloop()