document.addEventListener('DOMContentLoaded', function() {
    const attackerInput = document.getElementById('attacker-input');
    const attackerOutput = document.getElementById('attacker-output');
    const defenderInput = document.getElementById('defender-input');
    const defenderOutput = document.getElementById('defender-output');
    const threatsTableContainer = document.getElementById('threats-table-container');
    const threatsTbody = document.getElementById('threats-tbody');

    let lastThreats = [];
    let lastMessages = [];

    // Function to append to attacker output
    function appendAttacker(text) {
        attackerOutput.innerHTML += text + '<br>';
        attackerOutput.scrollTop = attackerOutput.scrollHeight;
    }

    // Function to append to defender output
    function appendDefender(text) {
        defenderOutput.innerHTML += text + '<br>';
        defenderOutput.scrollTop = defenderOutput.scrollHeight;
    }

    // Function to update threats table
    function updateThreatsTable(threats) {
        threatsTbody.innerHTML = '';
        threats.forEach(t => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${t.status}</td>
                <td>${t.severity}</td>
                <td>${t.ip}</td>
                <td>${t.attack}</td>
            `;
            threatsTbody.appendChild(row);
        });
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

    // Handle defender input
    defenderInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            const cmd = defenderInput.value.trim();
            defenderInput.value = '';
            appendDefender(`defender> ${cmd}`);

            fetch('/defender_command', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ command: cmd }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.show_table) {
                    updateThreatsTable(data.threats);
                    threatsTableContainer.style.display = 'block';
                    defenderOutput.style.display = 'none';
                } else {
                    threatsTableContainer.style.display = 'none';
                    defenderOutput.style.display = 'block';
                    appendDefender(data.output);
                }
                defenderInput.focus();
            });
        }
    });

    // Poll for threats (update table if visible)
    setInterval(() => {
        if (threatsTableContainer.style.display === 'block') {
            fetch('/defender_command', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ command: 'view' }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.show_table) {
                    updateThreatsTable(data.threats);
                }
            });
        }
    }, 1000);
});