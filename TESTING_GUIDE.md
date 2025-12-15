# Quick Testing Guide

Follow these steps to verify all data structures are working:

## Test 1: Priority Queue
1. Go to Attacker console
2. Launch these attacks:
   - `192.168.1.10` → `SQL_Injection` (HIGH)
   - `192.168.1.11` → `Port_Scan` (LOW)
   - `192.168.1.12` → `XSS_Attack` (MEDIUM)
3. Go to Defender console
4. Type: `view`
5. ✅ Verify threats appear sorted: HIGH → MEDIUM → LOW

## Test 2: Hash Map (Attack Counting)
1. Go to Defender console
2. Type: `stats`
3. ✅ Verify instant statistics display (O(1) lookup from hash map)

## Test 3: Hash Set (Auto-Blocking)
1. Go to Attacker console
2. Launch 3 attacks from same IP (e.g., `192.168.1.20`)
3. ✅ Verify auto-block message appears after 3rd attack
4. Try 4th attack from same IP
5. ✅ Verify attack is blocked

## Test 4: Linked List (Recent History)
1. Launch 5-10 attacks from different IPs
2. Go to Defender console
3. Type: `recent 5`
4. ✅ Verify last 5 attacks appear in chronological order

## Test 5: Graph (Pattern Recognition)
1. Launch attacks from multiple IPs:
   - `10.0.0.1` → launch 2+ attacks
   - `10.0.0.2` → launch 2+ attacks
   - `10.0.0.3` → launch 2+ attacks
2. Go to Defender console
3. Type: `patterns`
4. ✅ Verify clusters of related IPs appear
5. Type: `related 10.0.0.1`
6. ✅ Verify connected IPs are listed

## All Commands to Try

```
view           - See priority queue in action
stats          - See hash map lookups
recent 10      - See linked list traversal
patterns       - See graph clustering (DFS)
related <ip>   - See graph adjacency
blocked        - See hash set members
block <ip>     - See hash set insertion
unblock <ip>   - See hash set removal
help           - See all commands
```

## Expected Results

✅ All data structures working together seamlessly
✅ Fast O(1) operations for hash structures
✅ Efficient O(log n) for priority queue
✅ Pattern detection via graph traversal
✅ Chronological history via linked list

All requirements satisfied with minimal code!
