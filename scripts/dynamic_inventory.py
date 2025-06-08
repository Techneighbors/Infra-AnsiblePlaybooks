#!/usr/bin/env python3
"""
Dynamic Ansible Inventory for Homelab
Automatically discovers hosts and organizes them by detected services
"""

import json
import subprocess
import socket
import argparse
import yaml
from pathlib import Path
import concurrent.futures
from typing import Dict, List, Set
import ipaddress

class HomelabInventory:
    def __init__(self, config_file='config/discovery.yml'):
        self.config = self.load_config(config_file)
        self.inventory = {
            '_meta': {
                'hostvars': {}
            },
            'all': {
                'children': []
            }
        }
        
    def load_config(self, config_file: str) -> Dict:
        """Load discovery configuration"""
        default_config = {
            'networks': ['192.168.1.0/24'],
            'ports': {
                'ssh': [22, 2222],
                'web': [80, 443, 8080, 3000, 9090],
                'docker': [2375, 2376],
                'database': [3306, 5432, 27017, 6379],
                'monitoring': [9100, 9090, 3000],
                'media': [8096, 32400, 7878, 8989],
                'dns': [53],
                'vpn': [1194, 51820]
            },
            'timeout': 2,
            'max_workers': 50,
            'ansible_user': 'admin',
            'ansible_ssh_common_args': '-o StrictHostKeyChecking=no'
        }
        
        try:
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f)
                return {**default_config, **config}
        except FileNotFoundError:
            return default_config

    def scan_host(self, ip: str) -> Dict:
        """Scan a single host for open ports and services"""
        host_info = {
            'ip': ip,
            'hostname': None,
            'services': [],
            'open_ports': [],
            'ansible_host': ip,
            'ansible_user': self.config['ansible_user'],
            'ansible_ssh_common_args': self.config['ansible_ssh_common_args']
        }
        
        # Try to resolve hostname
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            host_info['hostname'] = hostname
        except socket.herror:
            pass
            
        # Scan common ports
        open_ports = []
        for category, ports in self.config['ports'].items():
            for port in ports:
                if self.check_port(ip, port):
                    open_ports.append(port)
                    if category not in host_info['services']:
                        host_info['services'].append(category)
        
        host_info['open_ports'] = open_ports
        
        # Only return hosts with SSH access
        if any(port in self.config['ports']['ssh'] for port in open_ports):
            return host_info
        return None

    def check_port(self, ip: str, port: int) -> bool:
        """Check if a port is open on a host"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.config['timeout'])
                result = sock.connect_ex((ip, port))
                return result == 0
        except Exception:
            return False

    def discover_hosts(self) -> List[Dict]:
        """Discover all hosts in configured networks"""
        all_hosts = []
        
        for network in self.config['networks']:
            print(f"Scanning network: {network}")
            network_obj = ipaddress.IPv4Network(network, strict=False)
            
            # Use ThreadPoolExecutor for parallel scanning
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.config['max_workers']) as executor:
                future_to_ip = {
                    executor.submit(self.scan_host, str(ip)): str(ip) 
                    for ip in network_obj.hosts()
                }
                
                for future in concurrent.futures.as_completed(future_to_ip):
                    result = future.result()
                    if result:
                        all_hosts.append(result)
                        print(f"Found host: {result['ip']} ({result.get('hostname', 'unknown')})")
        
        return all_hosts

    def organize_hosts(self, hosts: List[Dict]) -> Dict:
        """Organize hosts into logical groups"""
        groups = {
            'discovered': {'hosts': [], 'vars': {}},
            'webservers': {'hosts': [], 'vars': {}},
            'databases': {'hosts': [], 'vars': {}},
            'monitoring': {'hosts': [], 'vars': {}},
            'media_servers': {'hosts': [], 'vars': {}},
            'dns_servers': {'hosts': [], 'vars': {}},
            'vpn_servers': {'hosts': [], 'vars': {}},
            'docker_hosts': {'hosts': [], 'vars': {}},
            'production': {'hosts': [], 'vars': {}},
            'development': {'hosts': [], 'vars': {}}
        }
        
        for host in hosts:
            host_name = host.get('hostname') or f"host-{host['ip'].replace('.', '-')}"
            
            # Add to discovered group
            groups['discovered']['hosts'].append(host_name)
            
            # Categorize by services
            services = host.get('services', [])
            
            if 'web' in services:
                groups['webservers']['hosts'].append(host_name)
                
            if 'database' in services:
                groups['databases']['hosts'].append(host_name)
                
            if 'monitoring' in services:
                groups['monitoring']['hosts'].append(host_name)
                
            if 'media' in services:
                groups['media_servers']['hosts'].append(host_name)
                
            if 'dns' in services:
                groups['dns_servers']['hosts'].append(host_name)
                
            if 'vpn' in services:
                groups['vpn_servers']['hosts'].append(host_name)
                
            if 'docker' in services:
                groups['docker_hosts']['hosts'].append(host_name)
            
            # Categorize by environment (example logic)
            if 'prod' in host_name.lower() or '192.168.1.' in host['ip']:
                groups['production']['hosts'].append(host_name)
            elif 'dev' in host_name.lower() or 'test' in host_name.lower():
                groups['development']['hosts'].append(host_name)
            else:
                groups['production']['hosts'].append(host_name)  # Default to production
            
            # Add host variables
            self.inventory['_meta']['hostvars'][host_name] = {
                'ansible_host': host['ip'],
                'ansible_user': host.get('ansible_user', self.config['ansible_user']),
                'detected_services': services,
                'open_ports': host.get('open_ports', []),
                'discovery_timestamp': self.get_timestamp()
            }
        
        # Clean up empty groups
        return {k: v for k, v in groups.items() if v['hosts']}

    def get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()

    def generate_inventory(self) -> Dict:
        """Generate complete Ansible inventory"""
        hosts = self.discover_hosts()
        groups = self.organize_hosts(hosts)
        
        # Build inventory structure
        self.inventory['all']['children'] = list(groups.keys())
        
        for group_name, group_data in groups.items():
            self.inventory[group_name] = {
                'hosts': {host: {} for host in group_data['hosts']},
                'vars': group_data.get('vars', {})
            }
        
        return self.inventory

    def save_static_inventory(self, filename: str = 'inventory/discovered-hosts.yml'):
        """Save discovered inventory to static file"""
        inventory = self.generate_inventory()
        
        # Create directory if it doesn't exist
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        
        with open(filename, 'w') as f:
            yaml.dump(inventory, f, default_flow_style=False, indent=2)
        
        print(f"Static inventory saved to: {filename}")

def main():
    parser = argparse.ArgumentParser(description='Dynamic Homelab Inventory')
    parser.add_argument('--list', action='store_true', help='List all hosts')
    parser.add_argument('--host', help='Get variables for specific host')
    parser.add_argument('--save', help='Save to static inventory file', nargs='?', 
                       const='inventory/discovered-hosts.yml')
    parser.add_argument('--config', help='Configuration file', 
                       default='config/discovery.yml')
    
    args = parser.parse_args()
    
    inventory = HomelabInventory(args.config)
    
    if args.save:
        inventory.save_static_inventory(args.save)
    elif args.list:
        result = inventory.generate_inventory()
        print(json.dumps(result, indent=2))
    elif args.host:
        result = inventory.generate_inventory()
        host_vars = result.get('_meta', {}).get('hostvars', {}).get(args.host, {})
        print(json.dumps(host_vars, indent=2))
    else:
        result = inventory.generate_inventory()
        print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main() 