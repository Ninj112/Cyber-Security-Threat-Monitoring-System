# Quick Start Guide - Cyber Security Threat Monitoring System

## 🚀 Getting Started (3 Steps)

### Step 1: Install Flask
```bash
pip install flask
```

### Step 2: Run the Application
```bash
python app.py
```

### Step 3: Open Your Browser
Navigate to: **http://127.0.0.1:5000**

---

## 🎮 Attacker Console Quick Reference

### Basic Commands
| Command | Description | Example |
|---------|-------------|---------|
| `attack <ip> <type>` | Execute attack | `attack 192.168.1.100 SQL Injection` |
| `list` | Show all attack types | `list` |
| `help` | Show help | `help` |
| `clear` | Clear console | `clear` |

### Quick Attack Examples
```bash
# High severity attacks
attack 10.0.0.5 Remote Code Execution
attack 10.0.0.5 Ransomware Attempt
attack 10.0.0.5 SQL Injection

# Medium severity attacks  
attack 192.168.1.50 Brute Force Login
attack 192.168.1.50 DDOS Attempt

# Low severity attacks
attack 172.16.0.10 Port Scan
attack 172.16.0.10 Ping Sweep
```

**Tip**: After 3 attacks from the same IP, it will be auto-blocked!

---

## 🛡️ Defender Console Quick Reference

### Essential Commands
| Command | Description | Example |
|---------|-------------|---------|
| `view` | Show threat table | `view` |
| `stats` | Show statistics | `stats` |
| `blocked` | List blocked IPs | `blocked` |
| `isolate <ip>` | Isolate device | `isolate 192.168.1.100` |
| `block <ip>` | Block IP manually | `block 10.0.0.5` |
| `unblock <ip>` | Unblock IP | `unblock 10.0.0.5` |
| `alert <msg>` | Send alert | `alert Suspicious activity detected` |
| `clear` | Clear console | `clear` |
| `help` | Show help | `help` |

### Workflow Example
```bash
# 1. Check current threats
view

# 2. Check statistics
stats

# 3. Block a suspicious IP
block 192.168.1.100

# 4. Check blocked IPs
blocked

# 5. Send an alert
alert Multiple high-severity attacks detected

# 6. Later, unblock if needed
unblock 192.168.1.100
```

**Tip**: The threat table auto-refreshes every 2 seconds when viewing!

---

## 🎯 Common Use Cases

### Scenario 1: Simulate Multiple Attacks
**Attacker Console:**
```bash
attack 10.0.0.5 SQL Injection
attack 10.0.0.5 Remote Code Execution
attack 10.0.0.5 DDoS Attempt
```
→ IP will be auto-blocked after 3rd attack

**Defender Console:**
```bash
view
# You'll see all 3 attacks and the IP marked as "Blocked"
```

### Scenario 2: Manual Defense Response
**Defender Console:**
```bash
view                                    # See threats
isolate 192.168.1.100                  # Isolate suspicious IP
alert Isolated device 192.168.1.100    # Notify team
stats                                   # Check impact
```

### Scenario 3: Monitoring & Analysis
**Defender Console:**
```bash
view                    # Monitor threats in real-time
# Click column headers to sort by Status, Severity, IP, Attack, or Time
stats                   # View breakdown by severity
blocked                 # Check all blocked IPs
```

---

## 📊 Understanding the Interface

### Severity Levels
- 🔴 **HIGH** (Red) - Critical threats requiring immediate action
- 🟠 **MEDIUM** (Orange) - Moderate threats requiring monitoring  
- 🟢 **LOW** (Green) - Minor threats for awareness

### Status Indicators
- 🔴 **Active** (Red) - Threat is ongoing, IP not blocked
- ⚫ **Blocked** (Gray) - IP has been blocked

### Auto-Blocking Rules
- **Threshold**: 3 attacks from same IP
- **Actions Taken**:
  1. IP added to blocklist
  2. Device isolated from network
  3. Admin alert triggered
  4. All logged to JSON files

---

## 💡 Pro Tips

### For Attackers
1. Use **Tab** to autocomplete attack types
2. Use **↑** and **↓** arrows for command history
3. Type `list` to see all available attacks grouped by severity
4. Blocked IPs cannot execute new attacks

### For Defenders
1. **Sort threats** by clicking table column headers
2. **Auto-refresh** activates when viewing the threat table
3. Use `stats` to get a quick overview
4. Use `clear` to clean up message logs
5. `unblock` resets the attack counter for that IP

### Keyboard Shortcuts
- **Enter** - Execute command
- **↑/↓ Arrow Keys** - Navigate command history
- **Tab** - Autocomplete (attacker console)
- **Click anywhere** - Refocus input

---

## 🔧 Troubleshooting

### Problem: "IP is blocked"
**Solution**: Use defender console to unblock
```bash
unblock 192.168.1.100
```

### Problem: "Unknown attack type"
**Solution**: Type `list` in attacker console to see valid types

### Problem: Table not updating
**Solution**: 
1. Type `view` again to refresh
2. Auto-refresh works every 2 seconds when table is visible

### Problem: Port 5000 already in use
**Solution**: Edit `app.py` line 334:
```python
app.run(debug=True, host='127.0.0.1', port=5001)
```

---

## 📁 Data Files Location

All data stored in `data/` folder:
- `attack_log.json` - All attack history
- `blocked_ips.json` - Currently blocked IPs
- `threats.txt` - Attack type definitions

These files persist between sessions!

---

## 🎓 Learning Exercises

### Exercise 1: Test Auto-Blocking
1. Open attacker console
2. Execute 3 attacks from same IP
3. Try a 4th attack - it should be blocked
4. Check defender console to verify

### Exercise 2: Threat Management
1. Generate 10 different attacks from various IPs
2. Use defender `view` to monitor
3. Sort by severity
4. Block the highest severity IPs
5. Check `stats` to see the impact

### Exercise 3: Response Workflow
1. Simulate an attack wave
2. Use `view` to identify patterns
3. Use `isolate` on suspicious IPs
4. Use `alert` to notify team
5. Document findings with `stats`

---

## 📞 Need Help?

- Type `help` in any console
- Check the main [README.md](README.md) for detailed documentation
- Review [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) for technical details

---

**Remember**: This is a simulation tool for education. Use responsibly! 🎓
