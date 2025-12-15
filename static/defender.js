/**
 * Defender Console JavaScript
 * Handles threat monitoring and defense interface
 */

document.addEventListener('DOMContentLoaded', function() {
    const defenderInput = document.getElementById('defender-input');
    const defenderOutput = document.getElementById('defender-output');
    const threatsTableContainer = document.getElementById('threats-table-container');
    const threatsTbody = document.getElementById('threats-tbody');
    const threatsTable = document.getElementById('threats-table');
    
    const commandHistory = [];
    let historyIndex = -1;
    let sortKey = 'severity';
    let sortDirection = 'asc';  // asc for severity means HIGH first (priority 1)
    let autoRefresh = false;
    let refreshInterval = null;

    // Function to append output with color coding
    function appendOutput(text, className = '') {
        const span = document.createElement('span');
        if (className) {
            span.className = className;
        }
        span.innerHTML = text + '<br>';
        defenderOutput.appendChild(span);
        defenderOutput.scrollTop = defenderOutput.scrollHeight;
    }

    // Function to sort threats
    function sortThreats(threats) {
        // Severity priority for proper sorting
        const severityPriority = {
            'HIGH': 1,
            'MEDIUM': 2,
            'LOW': 3
        };
        
        // Status priority for proper sorting
        const statusPriority = {
            'Active': 1,
            'Blocked': 2
        };
        
        return threats.sort((a, b) => {
            let aVal = a[sortKey];
            let bVal = b[sortKey];
            
            // Special handling for time sorting
            if (sortKey === 'time') {
                aVal = new Date(aVal);
                bVal = new Date(bVal);
            }
            // Special handling for severity sorting
            else if (sortKey === 'severity') {
                aVal = severityPriority[aVal] || 999;
                bVal = severityPriority[bVal] || 999;
            }
            // Special handling for status sorting
            else if (sortKey === 'status') {
                aVal = statusPriority[aVal] || 999;
                bVal = statusPriority[bVal] || 999;
            }
            
            if (aVal < bVal) return sortDirection === 'asc' ? -1 : 1;
            if (aVal > bVal) return sortDirection === 'asc' ? 1 : -1;
            return 0;
        });
    }

    // Function to update threats table
    function updateThreatsTable(threats) {
        threats = sortThreats(threats);
        threatsTbody.innerHTML = '';
        
        if (threats.length === 0) {
            const row = document.createElement('tr');
            row.innerHTML = '<td colspan="5" style="text-align: center;">No threats detected</td>';
            threatsTbody.appendChild(row);
            return;
        }

        threats.forEach(threat => {
            const row = document.createElement('tr');
            const statusClass = threat.status === 'Blocked' ? 'blocked-status' : 'active-status';
            const severityClass = `severity-${threat.severity.toLowerCase()}`;
            
            row.innerHTML = `
                <td><span class="${statusClass}">${threat.status}</span></td>
                <td><span class="${severityClass}">${threat.severity}</span></td>
                <td>${threat.ip}</td>
                <td>${threat.attack}</td>
                <td>${threat.time}</td>
            `;
            threatsTbody.appendChild(row);
        });
    }

    // Add sorting to table headers
    const headers = threatsTable.querySelectorAll('th');
    headers.forEach((header, index) => {
        header.style.cursor = 'pointer';
        header.addEventListener('click', () => {
            const keys = ['status', 'severity', 'ip', 'attack', 'time'];
            const key = keys[index];
            
            if (sortKey === key) {
                sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
            } else {
                sortKey = key;
                sortDirection = 'asc';
            }
            
            // Update header indicators
            headers.forEach(h => h.classList.remove('sort-asc', 'sort-desc'));
            header.classList.add(`sort-${sortDirection}`);
            
            // Re-fetch and update table
            executeCommand('view', false);
        });
    });

    // Function to execute defender command
    function executeCommand(cmd, showPrompt = true) {
        if (showPrompt) {
            appendOutput(`defender@system:~$ ${cmd}`, 'prompt-text');
        }

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
                
                // Start auto-refresh when viewing table
                if (!autoRefresh && refreshInterval === null) {
                    autoRefresh = true;
                    refreshInterval = setInterval(() => {
                        if (threatsTableContainer.style.display === 'block') {
                            executeCommand('view', false);
                        }
                    }, 2000); // Refresh every 2 seconds
                }
            } else {
                threatsTableContainer.style.display = 'none';
                defenderOutput.style.display = 'block';
                
                // Stop auto-refresh when not viewing table
                if (autoRefresh && refreshInterval !== null) {
                    clearInterval(refreshInterval);
                    refreshInterval = null;
                    autoRefresh = false;
                }
                
                // Display output with proper formatting
                if (data.output) {
                    const lines = data.output.split('\n');
                    lines.forEach(line => {
                        if (line.startsWith('===')) {
                            appendOutput(line, 'info-text');
                        } else if (line.startsWith('✓')) {
                            appendOutput(line, 'success-text');
                        } else if (line.includes('HIGH')) {
                            appendOutput(line, 'error-text');
                        } else if (line.includes('MEDIUM')) {
                            appendOutput(line, 'warning-text');
                        } else if (line.includes('LOW')) {
                            appendOutput(line, 'success-text');
                        } else {
                            appendOutput(line, '');
                        }
                    });
                }
            }
            defenderInput.focus();
        })
        .catch(error => {
            appendOutput(`[ERROR] Network error: ${error}`, 'error-text');
        });
    }

    // Handle command input with history
    defenderInput.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowUp') {
            e.preventDefault();
            if (commandHistory.length > 0) {
                historyIndex = Math.min(historyIndex + 1, commandHistory.length - 1);
                defenderInput.value = commandHistory[commandHistory.length - 1 - historyIndex];
            }
        } else if (e.key === 'ArrowDown') {
            e.preventDefault();
            if (historyIndex > 0) {
                historyIndex--;
                defenderInput.value = commandHistory[commandHistory.length - 1 - historyIndex];
            } else {
                historyIndex = -1;
                defenderInput.value = '';
            }
        }
    });

    // Handle command execution
    defenderInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            const cmd = defenderInput.value.trim();
            if (!cmd) return;

            defenderInput.value = '';
            commandHistory.push(cmd);
            historyIndex = -1;

            if (cmd.toLowerCase() === 'clear') {
                defenderOutput.innerHTML = '<span class="info-text">Console cleared. Type \'help\' for commands</span><br>';
                threatsTableContainer.style.display = 'none';
                defenderOutput.style.display = 'block';
                
                // Stop auto-refresh on clear
                if (refreshInterval !== null) {
                    clearInterval(refreshInterval);
                    refreshInterval = null;
                    autoRefresh = false;
                }
            } else {
                executeCommand(cmd);
            }
        }
    });

    // Focus input on click anywhere
    document.addEventListener('click', function() {
        defenderInput.focus();
    });

    // Cleanup on page unload
    window.addEventListener('beforeunload', function() {
        if (refreshInterval !== null) {
            clearInterval(refreshInterval);
        }
    });
});