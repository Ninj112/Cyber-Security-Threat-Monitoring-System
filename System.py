import json
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Tuple
from src.common import ATTACK_SEVERITY_MAP, PRIORITY, Threat


class AttackSeverityTracker:
    """
    A system to store and track attack severity across the network.
    """
    def __init__(self):
        """Initialize the attack severity tracker."""
        self.attacks = []  # List of all tracked attacks
        self.severity_count = defaultdict(int)  # Count of attacks by severity
        self.ip_attacks = defaultdict(list)  # Attacks grouped by IP
        self.attack_type_count = defaultdict(int)  # Count of each attack type
        self.threat_queue = []  # Priority queue of threats

    def log_attack(self, ip: str, attack_type: str) -> Threat:
        """
        Log a new attack and determine its severity.

        Args:
            ip (str): The IP address of the attacker
            attack_type (str): The type of attack detected

        Returns:
            Threat: The threat object created for this attack
        """
        # Get severity from the map
        severity = ATTACK_SEVERITY_MAP.get(attack_type, "LOW")

        # Create a threat object
        threat = Threat(ip, attack_type, severity)

        # Log the attack with timestamp
        attack_record = {
            "timestamp": datetime.now().isoformat(),
            "ip": ip,
            "attack_type": attack_type,
            "severity": severity,
            "priority": threat.priority,
        }

        # Store the attack
        self.attacks.append(attack_record)
        self.severity_count[severity] += 1
        self.ip_attacks[ip].append(attack_record)
        self.attack_type_count[attack_type] += 1
        self.threat_queue.append(threat)

        # Sort threat queue by priority
        self.threat_queue.sort()

        return threat

    def get_severity_stats(self) -> Dict[str, int]:
        """
        Get statistics of attacks by severity level.

        Returns:
            Dict[str, int]: Count of attacks for each severity level
        """
        return dict(self.severity_count)

    def get_attacks_by_ip(self, ip: str) -> List[Dict]:
        """
        Get all attacks from a specific IP address.

        Args:
            ip (str): The IP address to query

        Returns:
            List[Dict]: List of attack records from that IP
        """
        return self.ip_attacks.get(ip, [])

    def get_critical_threats(self) -> List[Threat]:
        """
        Get all critical threats (HIGH severity).

        Returns:
            List[Threat]: Sorted list of HIGH severity threats
        """
        return [threat for threat in self.threat_queue if threat.severity == "HIGH"]

    def get_threats_by_severity(self, severity: str) -> List[Threat]:
        """
        Get all threats of a specific severity level.

        Args:
            severity (str): The severity level (HIGH, MEDIUM, LOW)

        Returns:
            List[Threat]: List of threats matching the severity
        """
        return [threat for threat in self.threat_queue if threat.severity == severity]

    def get_attack_type_frequency(self) -> Dict[str, int]:
        """
        Get frequency of each attack type.

        Returns:
            Dict[str, int]: Count of each attack type
        """
        return dict(self.attack_type_count)

    def get_top_attacking_ips(self, limit: int = 10) -> List[Tuple[str, int]]:
        """
        Get the top attacking IP addresses by frequency.

        Args:
            limit (int): Number of top IPs to return (default: 10)

        Returns:
            List[Tuple[str, int]]: List of (IP, count) tuples, sorted by count
        """
        ip_counts = [(ip, len(attacks)) for ip, attacks in self.ip_attacks.items()]
        return sorted(ip_counts, key=lambda x: x[1], reverse=True)[:limit]

    def get_sorted_threats(self) -> List[Threat]:
        """
        Get all threats sorted by priority (HIGH to LOW).

        Returns:
            List[Threat]: Sorted list of all threats
        """
        return sorted(self.threat_queue)

    def get_attack_summary(self) -> Dict:
        """
        Get a comprehensive summary of all attacks.

        Returns:
            Dict: Summary statistics including counts and top threats
        """
        return {
            "total_attacks": len(self.attacks),
            "severity_distribution": self.get_severity_stats(),
            "attack_type_frequency": self.get_attack_type_frequency(),
            "top_attacking_ips": self.get_top_attacking_ips(),
            "critical_threats_count": len(self.get_critical_threats()),
        }

    def clear_history(self):
        """Clear all stored attack history."""
        self.attacks.clear()
        self.severity_count.clear()
        self.ip_attacks.clear()
        self.attack_type_count.clear()
        self.threat_queue.clear()

    def export_to_json(self, filename: str = "attack_log.json"):
        """
        Export attack history to a JSON file.

        Args:
            filename (str): Name of the file to save to
        """
        data = {
            "total_attacks": len(self.attacks),
            "severity_distribution": self.get_severity_stats(),
            "attack_type_frequency": self.get_attack_type_frequency(),
            "attacks": self.attacks,
        }
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Attack log exported to {filename}")

    def get_threat_alert(self) -> str:
        """
        Generate a threat alert for the highest priority threat.

        Returns:
            str: Alert message describing the most critical threat
        """
        if not self.threat_queue:
            return "No active threats detected."

        critical_threat = self.threat_queue[0]
        return (
            f"🚨 ALERT: {critical_threat.attack} detected from {critical_threat.ip} "
            f"(Severity: {critical_threat.severity})"
        )


if __name__ == "__main__":
    # Example usage
    tracker = AttackSeverityTracker()

    # Simulate some attacks
    tracker.log_attack("192.168.1.100", "SQL Injection")
    tracker.log_attack("192.168.1.101", "Port Scan")
    tracker.log_attack("192.168.1.100", "DDoS Attempt")
    tracker.log_attack("192.168.1.102", "Brute Force Login")
    tracker.log_attack("192.168.1.101", "Ping Sweep")

    # Display summary
    print("=" * 50)
    print("ATTACK SEVERITY TRACKING SYSTEM")
    print("=" * 50)
    print(f"\n{tracker.get_threat_alert()}")
    print(f"\nTotal Attacks: {len(tracker.attacks)}")
    print(f"\nSeverity Distribution: {tracker.get_severity_stats()}")
    print(f"\nAttack Type Frequency: {tracker.get_attack_type_frequency()}")
    print(f"\nTop Attacking IPs: {tracker.get_top_attacking_ips()}")
    print(f"\nAll Threats (Sorted by Priority):")
    for threat in tracker.get_sorted_threats():
        print(
            f"  - {threat.attack} from {threat.ip} (Severity: {threat.severity}, Priority: {threat.priority})"
        )
    print(f"\nSummary: {tracker.get_attack_summary()}")
