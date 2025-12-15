document.addEventListener('DOMContentLoaded', function() {
    const attackerInput = document.getElementById('attacker-input');
    const attackerOutput = document.getElementById('attacker-output');

    // Function to append to attacker output
    function appendAttacker(text) {
        attackerOutput.innerHTML += text + '<br>';
        attackerOutput.scrollTop = attackerOutput.scrollHeight;
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
});