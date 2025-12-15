import json, time, tkinter as tk
from utils.loader import load_threats

THREAT_FILE = "data/threats.txt"
LOG_FILE = "data/attack_log.json"

threat_map = load_threats(THREAT_FILE)

def log_attack(ip, attack):
    entry = {
        "ip": ip,
        "attack": attack,
        "severity": threat_map.get(attack, "LOW"),
        "time": time.time()
    }

    try:
        with open(LOG_FILE, "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append(entry)

    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=2)

# -------- GUI --------
root = tk.Tk()
root.title("ATTACKER TERMINAL")
root.geometry("700x400")
root.configure(bg="black")

FONT = ("Courier New", 11)
FG = "#00ff00"

# Output area
terminal = tk.Text(
    root,
    bg="black",
    fg=FG,
    insertbackground=FG,
    font=FONT,
    state="disabled"
)
terminal.pack(fill=tk.BOTH, expand=True)

# Input
command = tk.Entry(
    root,
    bg="black",
    fg=FG,
    insertbackground=FG,
    font=FONT,
    borderwidth=0
)
command.pack(fill=tk.X)

# ---------- Terminal Functions ----------
def write(text):
    terminal.config(state="normal")
    terminal.insert(tk.END, text + "\n")
    terminal.see(tk.END)
    terminal.config(state="disabled")

def execute_command(event=None):
    cmd = command.get()
    command.delete(0, tk.END)

    write(f"> {cmd}")

    # VERY SIMPLE COMMAND PARSER
    if cmd.startswith("attack"):
        # example: attack 192.168.1.5 SQL Injection
        try:
            _, ip, *atype = cmd.split()
            attack_type = " ".join(atype)
            log_attack(ip, attack_type)  # YOUR EXISTING FUNCTION
            write("[+] Attack executed successfully")
        except:
            write("[!] Invalid command format")

    elif cmd == "help":
        write("Commands:")
        write(" attack <ip> <attack_type>")
        write(" help")
        write(" clear")

    elif cmd == "clear":
        terminal.config(state="normal")
        terminal.delete("1.0", tk.END)
        terminal.config(state="disabled")

    else:
        write("[!] Unknown command")

command.bind("<Return>", execute_command)

# ---------- Boot Message ----------
write("> Cyber Attack Console v1.0")
write("> Type 'help' for commands")

root.mainloop()