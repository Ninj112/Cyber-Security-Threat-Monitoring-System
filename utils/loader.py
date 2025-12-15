def load_threats(file_path):
    threat_map = {}
    with open(file_path, 'r') as f:
        for line in f:
            attack, severity = line.strip().split(',')
            threat_map[attack] = severity
    return threat_map
