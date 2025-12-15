import heapq

PRIORITY = {
    "HIGH": 1,
    "MEDIUM": 2,
    "LOW": 3
}

class Threat:
    "Represents a security threat with priority-based sorting."
    def __init__(self, ip, attack, severity, time):
        self.ip = ip
        self.attack = attack
        self.severity = severity
        self.priority = PRIORITY.get(severity, 3)
        self.time = time

    def __lt__(self, other):
        # Higher priority (lower number) comes first
        if self.priority != other.priority:
            return self.priority < other.priority
        # If same priority, earlier time comes first
        return self.time < other.time

    def __repr__(self):
        return f"Threat(ip={self.ip}, attack={self.attack}, severity={self.severity})"


class ThreatQueue:
    """Priority queue for managing threats based on severity."""
    def __init__(self):
        self.heap = []

    def push(self, threat):
        """Add a threat to the priority queue."""
        heapq.heappush(self.heap, threat)

    def pop(self):
        """Remove and return the highest priority threat."""
        if self.heap:
            return heapq.heappop(self.heap)
        return None

    def peek(self):
        """View the highest priority threat without removing it."""
        if self.heap:
            return self.heap[0]
        return None

    def all(self):
        """Return all threats sorted by priority."""
        return sorted(self.heap)

    def is_empty(self):
        """Check if the queue is empty."""
        return len(self.heap) == 0

    def size(self):
        """Return the number of threats in the queue."""
        return len(self.heap)
