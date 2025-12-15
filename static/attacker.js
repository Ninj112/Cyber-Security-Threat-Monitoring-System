/**
 * Attacker Console JavaScript
 * Handles attack simulation interface
 */

document.addEventListener('DOMContentLoaded', function() {
    const attackerInput = document.getElementById('attacker-input');
    const attackerOutput = document.getElementById('attacker-output');
    const commandHistory = [];
    let historyIndex = -1;

    // List of available attack types
    const attackTypes = [
        "SQL Injection",
        "Remote Code Execution",
        "Privilege Escalation",
        "Ransomware Attempt",
        "Zero-Day Exploit",
        "Data Exfiltration",
        "Command Injection",
        "Brute Force Login",
        "DDOS Attempt",
        "Cross-Site Scripting (XSS)",
        "Malware Download",
        "Unauthorized API Access",
        "Credential Stuffing",
        "Suspicious File Upload",
        "Port Scan",
        "Ping Sweep",
        "Banner Grabbing",
        "Directory Enumeration",
        "Suspicious Login Attempt",
        "Unknown Traffic Pattern"
    ];

    // Function to append output with color coding
    function appendOutput(text, className = '') {
        const span = document.createElement('span');
        if (className) {
            span.className = className;
        }
        span.innerHTML = text + '<br>';
        attackerOutput.appendChild(span);
        attackerOutput.scrollTop = attackerOutput.scrollHeight;
    }

    // Function to execute attack
    function executeAttack(ip, attack) {
        fetch('/attack', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ ip: ip, attack: attack }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                appendOutput(`[✓] Attack executed successfully`, 'success-text');
                appendOutput(`    Target: ${ip}`, 'info-text');
                appendOutput(`    Type: ${attack}`, 'info-text');
                appendOutput(`    Severity: ${data.severity}`, 'warning-text');
            } else if (data.status === 'blocked') {
                appendOutput(`[✗] ${data.message}`, 'error-text');
            } else {
                appendOutput(`[!] ${data.message || 'Attack failed'}`, 'error-text');
            }
        })
        .catch(error => {
            appendOutput(`[ERROR] Network error: ${error}`, 'error-text');
        });
    }

    // Function to show help
    function showHelp() {
        appendOutput('=== ATTACK CONSOLE COMMANDS ===', 'info-text');
        appendOutput('  attack <ip> <attack_type>', 'command-text');
        appendOutput('    Execute a cyber attack against target IP', '');
        appendOutput('', '');
        appendOutput('  list', 'command-text');
        appendOutput('    List all available attack types', '');
        appendOutput('', '');
        appendOutput('  clear', 'command-text');
        appendOutput('    Clear the console output', '');
        appendOutput('', '');
        appendOutput('  help', 'command-text');
        appendOutput('    Show this help message', '');
        appendOutput('', '');
        appendOutput('Example: attack 192.168.1.100 SQL Injection', 'info-text');
    }

    // Function to list attack types
    function listAttacks() {
        appendOutput('=== AVAILABLE ATTACK TYPES ===', 'info-text');
        appendOutput('', '');
        appendOutput('HIGH SEVERITY:', 'error-text');
        attackTypes.slice(0, 7).forEach(attack => {
            appendOutput(`  • ${attack}`, '');
        });
        appendOutput('', '');
        appendOutput('MEDIUM SEVERITY:', 'warning-text');
        attackTypes.slice(7, 14).forEach(attack => {
            appendOutput(`  • ${attack}`, '');
        });
        appendOutput('', '');
        appendOutput('LOW SEVERITY:', 'success-text');
        attackTypes.slice(14).forEach(attack => {
            appendOutput(`  • ${attack}`, '');
        });
    }

    // Handle command input
    attackerInput.addEventListener('keydown', function(e) {
        // Command history navigation
        if (e.key === 'ArrowUp') {
            e.preventDefault();
            if (commandHistory.length > 0) {
                historyIndex = Math.min(historyIndex + 1, commandHistory.length - 1);
                attackerInput.value = commandHistory[commandHistory.length - 1 - historyIndex];
            }
        } else if (e.key === 'ArrowDown') {
            e.preventDefault();
            if (historyIndex > 0) {
                historyIndex--;
                attackerInput.value = commandHistory[commandHistory.length - 1 - historyIndex];
            } else {
                historyIndex = -1;
                attackerInput.value = '';
            }
        } else if (e.key === 'Tab') {
            e.preventDefault();
            // Simple autocomplete for attack command
            if (attackerInput.value.startsWith('attack ')) {
                const parts = attackerInput.value.split(' ');
                if (parts.length >= 2) {
                    const partial = parts.slice(2).join(' ').toLowerCase();
                    const match = attackTypes.find(type => 
                        type.toLowerCase().startsWith(partial)
                    );
                    if (match) {
                        attackerInput.value = `attack ${parts[1]} ${match}`;
                    }
                }
            }
        }
    });
    // IP VALIDATION
function isValidIP(ip) {
    if (ip.includes("..")) return false;

    const parts = ip.split('.');
    if (parts.length !== 4) return false;

    for (const part of parts) {
        if (!/^\d+$/.test(part)) return false;
        const n = Number(part);
        if (n < 0 || n > 255) return false;
    }
    return true;
}

// Handle command execution
attackerInput.addEventListener('keydown', function (e) {
    if (e.key !== 'Enter') return;

    const cmd = attackerInput.value.trim();
    if (!cmd) return;

    attackerInput.value = '';
    commandHistory.push(cmd);
    historyIndex = -1;

    appendOutput(`attacker@system:~$ ${cmd}`, 'prompt-text');

    const parts = cmd.split(/\s+/);
    const command = parts[0].toLowerCase();

    if (command === 'attack') {
        if (parts.length < 3) {
            appendOutput('[!] Usage: attack <ip> <attack_type>', 'error-text');
            return;
        }

        const ip = parts[1];
        const attack = parts.slice(2).join(' ');

        if (!isValidIP(ip)) {
            appendOutput(`[!] Invalid IP address: ${ip}`, 'error-text');
            return;
        }

        executeAttack(ip, attack);
        return;
    }

    if (command === 'help') return showHelp();
    if (command === 'list') return listAttacks();
    if (command === 'clear') {
        attackerOutput.innerHTML = '';
        return;
    }

    appendOutput(`[!] Unknown command: '${command}'`, 'error-text');
});


    // Focus input on click anywhere
    document.addEventListener('click', function() {
        attackerInput.focus();
    });
});