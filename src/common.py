PRIORITY = {
    "HIGH": 1,
    "MEDIUM": 2,
    "LOW": 3,
}

ATTACK_SEVERITY_MAP = {
    "SQL Injection": "HIGH",
    "Remote Code Execution": "HIGH",
    "Ransomware Attempt": "HIGH",
    "Zero-Day Exploit": "HIGH",
    "DDoS Attempt": "HIGH",
    "Brute Force Login": "MEDIUM",
    "Credential Stuffing": "MEDIUM",
    "Suspicious Login Attempt": "MEDIUM",
    "Port Scan": "LOW",
    "Ping Sweep": "LOW",
    "Banner Grabbing": "LOW",
    "Directory Enumeration": "LOW",
}


class Threat:
    def __init__(self, ip: str, attack: str, severity: str):
        self.ip = ip
        self.attack = attack
        self.severity = severity
        self.priority = PRIORITY.get(severity, PRIORITY["LOW"])

    def __lt__(self, other):
        return self.priority < other.priority
