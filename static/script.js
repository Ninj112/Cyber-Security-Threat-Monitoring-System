document.addEventListener('DOMContentLoaded', function() {
    const attackerInput = document.getElementById('attacker-input');
    const attackerOutput = document.getElementById('attacker-output');
    const defenderOutput = document.getElementById('defender-output');

    let lastThreats = [];
    let lastMessages = [];

    // Function to append to attacker output
    function appendAttacker(text) {
        attackerOutput.innerHTML += text + '<br>';
        attackerOutput.scrollTop = attackerOutput.scrollHeight;
    }

    // Function to update defender output
    function updateDefender(threats, messages) {
        let output = '> Defender Monitoring Console<br>> Waiting for threats...<br>';
        threats.forEach(t => {
            output += `[${t.severity}] ${t.ip} | ${t.attack}<br>`;
        });
        messages.forEach(m => {
            output += m + '<br>';
        });
        defenderOutput.innerHTML = output;
        defenderOutput.scrollTop = defenderOutput.scrollHeight;
    }

    // Handle attacker input
    attackerInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            const cmd = attackerInput.value.trim();
            attackerInput.value = '';
            appendAttacker(`> ${cmd}`);

            if (cmd.startsWith('attack ')) {
                const parts = cmd.split(' ');
                if (parts.length >= 3) {
                    const ip = parts[1];
                    const attack = parts.slice(2).join(' ');
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
                            appendAttacker('[+] Attack executed successfully');
                        } else if (data.status === 'blocked') {
                            appendAttacker(`[!] ${data.message}`);
                        } else {
                            appendAttacker('[!] Error executing attack');
                        }
                    });
                } else {
                    appendAttacker('[!] Invalid command format');
                }
            } else if (cmd === 'help') {
                appendAttacker('Commands:');
                appendAttacker(' attack <ip> <attack_type>');
                appendAttacker(' help');
                appendAttacker(' clear');
            } else if (cmd === 'clear') {
                attackerOutput.innerHTML = '> Cyber Attack Console v1.0<br>> Type \'help\' for commands<br>';
            } else {
                appendAttacker('[!] Unknown command');
            }
        }
    });

    // Poll for threats
    setInterval(() => {
        fetch('/threats')
        .then(response => response.json())
        .then(data => {
            const threats = data.threats;
            const messages = data.messages;
            if (JSON.stringify(threats) !== JSON.stringify(lastThreats) || JSON.stringify(messages) !== JSON.stringify(lastMessages)) {
                updateDefender(threats, messages);
                lastThreats = threats;
                lastMessages = messages;
            }
        });
    }, 1000);
});