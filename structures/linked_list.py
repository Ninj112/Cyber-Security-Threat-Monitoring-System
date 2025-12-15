class Node:
    """Node for linked list implementation."""
    def __init__(self, data):
        self.data = data
        self.next = None


class ThreatLinkedList:
    """Linked list for storing threat history."""
    def __init__(self):
        self.head = None
        self._size = 0

    def add(self, threat):
        """Add a threat to the beginning of the list."""
        node = Node(threat)
        node.next = self.head
        self.head = node
        self._size += 1

    def remove(self, threat):
        """Remove the first occurrence of a threat from the list."""
        current = self.head
        prev = None
        
        while current:
            if current.data == threat:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                self._size -= 1
                return True
            prev = current
            current = current.next
        return False

    def find(self, condition):
        """Find the first threat matching a condition (function)."""
        current = self.head
        while current:
            if condition(current.data):
                return current.data
            current = current.next
        return None

    def to_list(self):
        """Convert linked list to Python list."""
        current = self.head
        result = []
        while current:
            result.append(current.data)
            current = current.next
        return result

    def is_empty(self):
        """Check if the linked list is empty."""
        return self.head is None

    def size(self):
        """Return the number of elements in the list."""
        return self._size

    def clear(self):
        """Remove all elements from the list."""
        self.head = None
        self._size = 0
