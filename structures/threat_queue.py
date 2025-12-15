import heapq

PRIORITY = {
    "CRITICAL": 0,
    "HIGH": 1,
    "MEDIUM": 2,
    "LOW": 3
}

class Threat:
    def __init__(self, ip, attack, severity, time):
        self.ip = ip
        self.attack = attack
        self.severity = severity
        self.priority = PRIORITY[severity]
        self.time = time

    def __lt__(self, other):
        return self.priority < other.priority


class ThreatQueue:
    def __init__(self):
        self.heap = []

    def push(self, threat):
        heapq.heappush(self.heap, threat)

    def pop(self):
        return heapq.heappop(self.heap)

    def all(self):
        return sorted(self.heap)
