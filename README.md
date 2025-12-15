# 🛡️ Cyber Security Threat Monitoring System

A real-time web-based cybersecurity monitoring system that simulates attack scenarios and defensive responses using advanced data structures for threat management.

## 📋 Features

### Core Functionality
- **Real-time Threat Monitoring**: Track and visualize cyber attacks as they occur
- **Priority-based Threat Queue**: Automatically prioritizes threats based on severity (HIGH, MEDIUM, LOW)
- **Automated Defense**: Auto-blocking of malicious IPs after threshold breaches
- **Interactive Consoles**: Separate interfaces for attackers and defenders
- **Persistent Storage**: All attacks and blocked IPs are saved to JSON files

### Data Structures
- **Priority Queue (Heap)**: Efficient threat prioritization using `heapq`
- **Linked List**: Historical threat tracking and management
- **Hash Sets**: Fast IP lookup for blocking and attack counting

## 🏗️ Project Structure

```
Cyber-Security-Threat-Monitoring-System/
├── app.py                      # Main Flask application
├── System.py                   # System tracking classes (optional)
├── data/
│   ├── attack_log.json        # Logged attacks
│   ├── blocked_ips.json       # Blocked IP addresses
│   └── threats.txt            # Attack type definitions
├── src/
│   └── common.py              # Common data structures and constants
├── structures/
│   ├── linked_list.py         # Linked list implementation
│   └── threat_queue.py        # Priority queue implementation
├── templates/
│   ├── index.html             # Landing page
│   ├── attacker.html          # Attacker console
│   └── defender.html          # Defender console
├── static/
│   ├── attacker.js            # Attacker console logic
│   ├── defender.js            # Defender console logic
│   └── style.css              # Terminal styling
└── utils/
    └── loader.py              # Utility functions
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7+
- Flask

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Cyber-Security-Threat-Monitoring-System
   ```

2. **Install dependencies**
   ```bash
   pip install flask
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   Open your browser and navigate to: `http://127.0.0.1:5000`

## 💻 Usage

### Attacker Console

Access the attacker console to simulate cyber attacks.

**Available Commands:**
- `attack <ip> <attack_type>` - Execute an attack
  - Example: `attack 192.168.1.100 SQL Injection`
- `list` - Show all available attack types
- `help` - Display help information
- `clear` - Clear console output

**Attack Types:**
- **HIGH Severity**: SQL Injection, Remote Code Execution, Ransomware Attempt, etc.
- **MEDIUM Severity**: Brute Force Login, DDoS Attempt, XSS, etc.
- **LOW Severity**: Port Scan, Ping Sweep, Directory Enumeration, etc.

### Defender Console

Monitor threats and take defensive actions.

**Available Commands:**
- `view` - Display all threats in a sortable table
- `stats` - Show threat statistics
- `blocked` - List all blocked IPs
- `isolate <ip>` - Isolate a device from the network
- `block <ip>` - Manually block an IP address
- `unblock <ip>` - Unblock an IP address
- `alert <message>` - Send alert to security team
- `clear` - Clear console output
- `help` - Display help information

## 🔧 Technical Details

### Threat Prioritization

The system uses a min-heap priority queue where:
- **HIGH** severity = Priority 1
- **MEDIUM** severity = Priority 2
- **LOW** severity = Priority 3

Lower priority numbers are processed first, ensuring critical threats receive immediate attention.

### Auto-blocking Mechanism

- Default threshold: **3 attacks** from the same IP
- When threshold is reached:
  1. IP is automatically blocked
  2. Device is isolated from the network
  3. Admin alert is triggered
  4. All actions are logged

### Data Persistence

- `attack_log.json`: Stores all attack attempts with timestamps
- `blocked_ips.json`: Maintains list of blocked IP addresses
- `threats.txt`: Defines attack types and their severity levels

## 📊 API Endpoints

### Frontend Routes
- `GET /` - Landing page
- `GET /attacker` - Attacker console
- `GET /defender` - Defender console

### API Routes
- `POST /attack` - Log a new attack
  ```json
  {
    "ip": "192.168.1.100",
    "attack": "SQL Injection"
  }
  ```

- `GET /threats` - Retrieve all current threats
- `POST /defender_command` - Execute defender command
  ```json
  {
    "command": "view"
  }
  ```

- `GET /status` - Get system status

## 🎨 UI Features

- **Matrix-style Terminal Interface**: Green text on black background
- **Real-time Updates**: Defender console auto-refreshes every 2 seconds
- **Sortable Threat Table**: Click column headers to sort
- **Command History**: Use arrow keys to navigate previous commands
- **Tab Completion**: Partial autocomplete for attack types
- **Visual Indicators**: Color-coded severity levels and status

## 🔒 Security Notes

⚠️ **Important**: This is a **simulation tool** for educational purposes only. Do not use it for actual security monitoring or penetration testing without proper authorization.

## 📝 Configuration

Edit these constants in `app.py` to customize behavior:

```python
THRESHOLD = 3  # Number of attacks before auto-blocking
LOG_FILE = "data/attack_log.json"
THREAT_FILE = "data/threats.txt"
BLOCKED_FILE = "data/blocked_ips.json"
```

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Change port in app.py
   app.run(debug=True, host='127.0.0.1', port=5001)
   ```

2. **Data files not found**
   - The application auto-creates data files on first run
   - Ensure write permissions in the project directory

3. **Flask not found**
   ```bash
   pip install flask
   ```

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional attack types
- Machine learning threat prediction
- Database integration
- User authentication
- Network visualization
- Export reports functionality

## 📄 License

This project is for educational purposes. Use responsibly.

## 👥 Authors

- Developed as a cybersecurity educational tool
- Demonstrates practical application of data structures in security contexts

## 🙏 Acknowledgments

- Flask framework for web development
- Matrix-inspired terminal design
- Cybersecurity community for threat classification standards

---

**Note**: This system is designed for learning and demonstration purposes. Always follow ethical guidelines and obtain proper authorization before conducting any security testing.
