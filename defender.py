import tkinter as tk
from tkinter import ttk, messagebox
import heapq

# ---------------- Priority Map ----------------
PRIORITY = {
    "HIGH": 1,
    "MEDIUM": 2,
    "LOW": 3
}

# ---------------- Threat Class ----------------
class Threat:
    def __init__(self, ip, attack, severity):
        self.ip = ip
        self.attack = attack
        self.severity = severity
        self.priority = PRIORITY[severity]

    def __lt__(self, other):
        return self.priority < other.priority


# ---------------- Defender GUI ----------------
class DefenderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cybersecurity Defender")
        self.root.geometry("650x500")

        self.queue = []

        # Title
        tk.Label(root, text="Incoming Threats", font=("Arial", 16, "bold")).pack(pady=10)

        # Table
        self.table = ttk.Treeview(
            root, columns=("IP", "Attack", "Severity"), show="headings"
        )

        self.table.heading("IP", text="IP Address")
        self.table.heading("Attack", text="Attack Type")
        self.table.heading("Severity", text="Severity")

        self.table.column("IP", width=200)
        self.table.column("Attack", width=220)
        self.table.column("Severity", width=120)

        self.table.pack(pady=10)

        # Add threat button
        tk.Button(root, text="Receive Test Threat", command=self.add_threat).pack(pady=5)

        # Action label
        tk.Label(root, text="Choose Action", font=("Arial", 12)).pack(pady=10)

        # Action buttons (ALL FOUR)
        tk.Button(root, text="Block IP", width=18,
                  command=lambda: self.handle("Blocked IP")).pack(pady=3)

        tk.Button(root, text="Alert Admin", width=18,
                  command=lambda: self.handle("Admin Alerted")).pack(pady=3)

        tk.Button(root, text="Isolate Host", width=18,
                  command=lambda: self.handle("Host Isolated")).pack(pady=3)

        tk.Button(root, text="Ignore", width=18,
                  command=lambda: self.handle("Ignored")).pack(pady=3)

    # ---------------- Add Threat ----------------
    def add_threat(self):
        threats = [
            Threat("10.0.0.5", "SQL Injection", "HIGH"),
            Threat("172.16.1.20", "Brute Force Login", "MEDIUM"),
            Threat("196.251.100.12", "Port Scan", "LOW")
        ]

        heapq.heappush(self.queue, threats[len(self.queue) % 3])
        self.refresh()

    # ---------------- Refresh Table ----------------
    def refresh(self):
        self.table.delete(*self.table.get_children())
        for t in sorted(self.queue):
            self.table.insert("", "end", values=(t.ip, t.attack, t.severity))

    # ---------------- Handle Threat ----------------
    def handle(self, action):
        selected = self.table.selection()

        if not selected:
            messagebox.showwarning("Warning", "Please select a threat first.")
            return

        ip = self.table.item(selected[0])["values"][0]

        for t in self.queue:
            if t.ip == ip:
                self.queue.remove(t)
                heapq.heapify(self.queue)
                break

        self.refresh()

        messagebox.showinfo("Handled", f"{action}\nIP: {ip}")


# ---------------- Run App ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = DefenderGUI(root)
    root.mainloop()