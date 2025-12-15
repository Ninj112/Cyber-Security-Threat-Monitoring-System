import heapq

PRIORITY = {"HIGH": 1, "MEDIUM": 2, "LOW": 3}

class Threat:
    def __init__(self, ip, attack, severity, time):
        self.ip = ip
        self.attack = attack
        self.severity = severity
        self.priority = PRIORITY.get(severity, 3)
        self.time = time

    def __lt__(self, other):
        return self.priority < other.priority if self.priority != other.priority else self.time < other.time


class ThreatQueue:
    def __init__(self):
        self.heap = []

    def push(self, threat):
        heapq.heappush(self.heap, threat)

    def pop(self):
        return heapq.heappop(self.heap) if self.heap else None

    def all(self):
        return sorted(self.heap)

    def size(self):
        return len(self.heap)
