"""Simple Linked List for Threat Logging"""

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class ThreatLinkedList:
    def __init__(self):
        self.head = None
        self.size = 0
    
    def add(self, data):
        """Add threat to the front of the list"""
        node = Node(data)
        node.next = self.head
        self.head = node
        self.size += 1
    
    def get_recent(self, n=10):
        """Get n most recent threats"""
        result = []
        current = self.head
        while current and len(result) < n:
            result.append(current.data)
            current = current.next
        return result
