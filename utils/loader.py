"""Utility functions for loading threat data."""

def load_threats(file_path):
    """
    Load threat definitions from a file.
    
    Args:
        file_path: Path to the threats.txt file
        
    Returns:
        Dictionary mapping attack types to severity levels
    """
    threat_map = {}
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and ',' in line:
                    attack, severity = line.split(',', 1)
                    threat_map[attack.strip()] = severity.strip()
    except FileNotFoundError:
        print(f"Warning: Threat file {file_path} not found. Using empty threat map.")
    except Exception as e:
        print(f"Error loading threats: {e}")
    return threat_map
