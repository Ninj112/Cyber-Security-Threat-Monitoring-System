"""Simple Graph for Threat Pattern Recognition"""

class ThreatGraph:
    def __init__(self):
        self.graph = {}  # adjacency list: {ip: [related_ips]}
    
    def add_connection(self, ip1, ip2):
        """Connect two IPs (e.g., similar attack patterns)"""
        if ip1 not in self.graph:
            self.graph[ip1] = []
        if ip2 not in self.graph:
            self.graph[ip2] = []
        
        if ip2 not in self.graph[ip1]:
            self.graph[ip1].append(ip2)
        if ip1 not in self.graph[ip2]:
            self.graph[ip2].append(ip1)
    
    def get_related(self, ip):
        """Get IPs with related attack patterns"""
        return self.graph.get(ip, [])
    
    def find_patterns(self):
        """Find clusters of related attacks"""
        visited = set()
        patterns = []
        
        for ip in self.graph:
            if ip not in visited:
                cluster = self._dfs(ip, visited)
                if len(cluster) > 1:  # Only clusters with multiple IPs
                    patterns.append(cluster)
        
        return patterns
    
    def _dfs(self, ip, visited):
        """Depth-first search to find connected IPs"""
        visited.add(ip)
        cluster = [ip]
        
        for neighbor in self.graph.get(ip, []):
            if neighbor not in visited:
                cluster.extend(self._dfs(neighbor, visited))
        
        return cluster
