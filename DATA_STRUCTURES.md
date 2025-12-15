# Data Structures Implementation

This project implements all required data structures per the cybersecurity project guidelines:

## 1. Priority Queue (Threat Prioritization)
**File:** `structures/threat_queue.py`
**Purpose:** Rank threats based on severity for triage
**Implementation:**
- Uses Python's `heapq` module for efficient priority queue
- Threats sorted by: HIGH (1) > MEDIUM (2) > LOW (3)
- O(log n) insertion and removal

**Usage:**
```python
queue.push(threat)  # Add threat with priority
threat = queue.pop()  # Get highest priority threat
```

## 2. Hash Map (Fast Threat Retrieval)
**File:** `app.py`
**Purpose:** Efficient lookups and attack counting
**Implementations:**
- `threat_map` - Maps attack types to severity levels
- `attack_counts` - Tracks attack frequency per IP
- Both use Python dictionaries (O(1) average lookup)

**Usage:**
```python
severity = threat_map["SQL_Injection"]  # O(1) lookup
attack_counts[ip] += 1  # O(1) increment
```

## 3. Hash Set (Duplicate Detection & Blocking)
**File:** `app.py`
**Purpose:** Track unique threats and blocked IPs
**Implementations:**
- `seen` - Prevents duplicate threat logging
- `blocked_ips` - Fast IP blocking checks
- Both use Python sets (O(1) membership testing)

**Usage:**
```python
if ip not in blocked_ips:  # O(1) check
    blocked_ips.add(ip)  # O(1) insertion
```

## 4. Linked List (Dynamic Threat Logging)
**File:** `structures/linked_list.py`
**Purpose:** Maintain chronological threat history
**Implementation:**
- Singly linked list with head pointer
- New threats added at front (O(1) insertion)
- Efficient retrieval of recent attacks

**Usage:**
```python
threat_history.add(attack_data)  # O(1) add
recent = threat_history.get_recent(10)  # O(n) get last n
```

## 5. Graph (Pattern Recognition)
**File:** `structures/threat_graph.py`
**Purpose:** Identify attack patterns and related IPs
**Implementation:**
- Adjacency list representation using dictionaries
- DFS algorithm for cluster detection
- Connects IPs with similar attack patterns

**Usage:**
```python
threat_graph.add_connection(ip1, ip2)  # Connect related IPs
patterns = threat_graph.find_patterns()  # Find attack clusters
related = threat_graph.get_related(ip)  # Get connected IPs
```

## Data Structure Summary

| Structure | Location | Time Complexity | Use Case |
|-----------|----------|----------------|----------|
| Priority Queue | threat_queue.py | O(log n) push/pop | Threat triage |
| Hash Map | app.py | O(1) average | Fast lookups |
| Hash Set | app.py | O(1) average | Blocking/dedup |
| Linked List | linked_list.py | O(1) add, O(n) read | Recent history |
| Graph | threat_graph.py | O(V+E) DFS | Pattern analysis |

## New Defender Commands

- `recent [n]` - Show n recent attacks from linked list
- `patterns` - Display attack patterns found by graph analysis
- `related <ip>` - Show IPs with similar attack patterns

All data structures work together to provide comprehensive threat monitoring and analysis.
