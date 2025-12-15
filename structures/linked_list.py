class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class ThreatLinkedList:
    def __init__(self):
        self.head = None

    def add(self, threat):
        node = Node(threat)
        node.next = self.head
        self.head = node

    def to_list(self):
        current = self.head
        result = []
        while current:
            result.append(current.data)
            current = current.next
        return result
