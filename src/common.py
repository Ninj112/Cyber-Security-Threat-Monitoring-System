"""Common data structures and constants for the threat monitoring system."""

PRIORITY = {
    "HIGH": 1,
    "MEDIUM": 2,
    "LOW": 3,
}

ATTACK_SEVERITY_MAP = {
    # HIGH severity attacks
    "SQL Injection": "HIGH",
    "Remote Code Execution": "HIGH",
    "Privilege Escalation": "HIGH",
    "Ransomware Attempt": "HIGH",
    "Zero-Day Exploit": "HIGH",
    "Data Exfiltration": "HIGH",
    "Command Injection": "HIGH",
    "DDoS Attempt": "HIGH",
    
    # MEDIUM severity attacks
    "Brute Force Login": "MEDIUM",
    "DDOS Attempt": "MEDIUM",
    "Cross-Site Scripting (XSS)": "MEDIUM",
    "Malware Download": "MEDIUM",
    "Unauthorized API Access": "MEDIUM",
    "Credential Stuffing": "MEDIUM",
    "Suspicious File Upload": "MEDIUM",
    
    # LOW severity attacks
    "Port Scan": "LOW",
    "Ping Sweep": "LOW",
    "Banner Grabbing": "LOW",
    "Directory Enumeration": "LOW",
    "Suspicious Login Attempt": "LOW",
    "Unknown Traffic Pattern": "LOW",
}


class Threat:
    """Represents a security threat."""
    def __init__(self, ip: str, attack: str, severity: str):
        self.ip = ip
        self.attack = attack
        self.severity = severity
        self.priority = PRIORITY.get(severity, PRIORITY["LOW"])

    def __lt__(self, other):
        """Compare threats by priority for sorting."""
        return self.priority < other.priority

    def __repr__(self):
        return f"Threat(ip={self.ip}, attack={self.attack}, severity={self.severity})"
