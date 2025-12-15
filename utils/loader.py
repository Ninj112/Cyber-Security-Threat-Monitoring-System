def load_threats(file_path):
    threat_map = {}
    try:
        with open(file_path, 'r') as f:
            for line in f:
                if ',' in line:
                    attack, severity = line.strip().split(',', 1)
                    threat_map[attack.strip()] = severity.strip()
    except:
        pass
    return threat_map
