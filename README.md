# Infra-AnsiblePlaybooks

Infrastructure automation playbooks using Ansible for system administration and configuration management.

## Overview

This repository contains Ansible playbooks for automating common infrastructure tasks including system updates, configuration management, and security hardening.

## Prerequisites

- Ansible 2.9+ installed on the control node
- SSH access to target hosts
- Sudo privileges on target systems
- Python 3.6+ on target hosts

## Directory Structure

```
├── playbooks/          # Ansible playbooks
├── inventory/          # Inventory files (to be added)
├── group_vars/         # Group variables (to be added)
├── host_vars/          # Host variables (to be added)
└── roles/              # Custom roles (to be added)
```

## Usage

### Automated Inventory Discovery

**Linux/macOS:**

```bash
# Quick setup and network scan
./scripts/homelab-discover setup
./scripts/homelab-discover scan

# Update inventory automatically
./scripts/homelab-discover update

# Generate visual report
./scripts/homelab-discover report

# Use dynamic inventory directly
ansible-playbook -i scripts/dynamic_inventory.py playbooks/update-apt-packages.yml
```

**Windows (PowerShell):**

```powershell
# Run Python scripts directly
python scripts/dynamic_inventory.py --list
python scripts/dynamic_inventory.py --save inventory/discovered-hosts.yml

# Run inventory management playbook
ansible-playbook playbooks/inventory-management.yml

# Use with other playbooks
ansible-playbook -i scripts/dynamic_inventory.py playbooks/update-apt-packages.yml
```

### Running Playbooks

```bash
# Update packages on all discovered hosts
ansible-playbook -i inventory/discovered-hosts.yml playbooks/update-apt-packages.yml

# Run with specific tags
ansible-playbook -i inventory/discovered-hosts.yml playbooks/update-apt-packages.yml --tags update

# Check mode (dry run)
ansible-playbook -i inventory/discovered-hosts.yml playbooks/update-apt-packages.yml --check

# Use dynamic inventory for real-time discovery
ansible-playbook -i scripts/dynamic_inventory.py playbooks/security-hardening.yml
```

### Available Playbooks

#### Core Infrastructure

- `update-apt-packages.yml` - Updates and upgrades APT packages on Debian/Ubuntu systems
- `security-hardening.yml` - Comprehensive security hardening (SSH, firewall, fail2ban, etc.)
- `docker-setup.yml` - Install and configure Docker with best practices
- `backup-setup.yml` - Automated backup solution using restic
- `monitoring-setup.yml` - Complete monitoring stack (Prometheus + Grafana + Node Exporter)

#### Planned Playbooks

- `nginx-reverse-proxy.yml` - Nginx reverse proxy with SSL termination
- `pihole-setup.yml` - Pi-hole DNS ad blocker installation
- `vpn-wireguard.yml` - WireGuard VPN server setup
- `media-server.yml` - Plex/Jellyfin media server installation
- `git-server.yml` - Self-hosted Git server (Gitea/GitLab)
- `database-setup.yml` - MySQL/PostgreSQL database server
- `file-sharing.yml` - Samba/NFS file sharing setup
- `certificates.yml` - Let's Encrypt SSL certificate management
- `user-management.yml` - System user and SSH key management
- `log-aggregation.yml` - Centralized logging with ELK stack

## Best Practices

- Always test playbooks in a development environment first
- Use `--check` mode for dry runs
- Tag your tasks for selective execution
- Implement proper error handling
- Use vaults for sensitive data

## Contributing

1. Test all changes in a development environment
2. Follow Ansible best practices and coding standards
3. Update documentation when adding new playbooks
4. Use descriptive commit messages

## Security

- Store sensitive data in Ansible Vault
- Use SSH key authentication
- Implement least privilege access
- Regularly review and audit playbook permissions
