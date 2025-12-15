document.addEventListener('DOMContentLoaded', function() {
    const defenderInput = document.getElementById('defender-input');
    const defenderOutput = document.getElementById('defender-output');
    const threatsTableContainer = document.getElementById('threats-table-container');
    const threatsTbody = document.getElementById('threats-tbody');

    // Function to append to defender output
    function appendDefender(text) {
        defenderOutput.innerHTML += text + '<br>';
        defenderOutput.scrollTop = defenderOutput.scrollHeight;
    }

    // Typing effect for welcome message
    const welcomeText = "Welcome to Defender Monitoring Console\nType 'help' for commands";
    let i = 0;
    const typeWriter = () => {
        if (i < welcomeText.length) {
            defenderOutput.innerHTML = welcomeText.substring(0, i + 1).replace(/\n/g, '<br>');
            i++;
            setTimeout(typeWriter, 50);
        }
    };
    typeWriter();

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
                <td>${t.time}</td>
            `;
            threatsTbody.appendChild(row);
        });
    }

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