# ⚡ Semaphore Quick Deployment Reference

## 🚀 Quick Setup Checklist

### 1. Repository Setup

- [ ] Push code to Git repository
- [ ] Verify all playbooks are present
- [ ] Check `ansible.cfg` configuration

### 2. Semaphore Configuration

- [ ] Create project: "Homelab Infrastructure"
- [ ] Add repository: Link to your Git repo
- [ ] Add SSH key for host access
- [ ] Create environment: "Production"

### 3. Essential Templates to Create

| Template Name           | Playbook                   | Inventory | Purpose                 |
| ----------------------- | -------------------------- | --------- | ----------------------- |
| **Inventory Discovery** | `inventory-management.yml` | localhost | Discover hosts          |
| **Security Hardening**  | `security-hardening.yml`   | Dynamic   | SSH, firewall, fail2ban |
| **System Updates**      | `update-apt-packages.yml`  | Dynamic   | Package updates         |
| **Docker Setup**        | `docker-setup.yml`         | Dynamic   | Docker installation     |
| **Backup Solution**     | `backup-setup.yml`         | Dynamic   | Restic backup setup     |
| **Monitoring Stack**    | `monitoring-setup.yml`     | Dynamic   | Prometheus + Grafana    |
| **Validation Checks**   | `validation-checks.yml`    | Dynamic   | Verify deployment       |

### 4. Deployment Order

```
1. Inventory Discovery → 2. Security Hardening → 3. System Updates
                                    ↓
4. Docker Setup (parallel) ← 5. Backup Solution ← 6. Monitoring Stack
                                    ↓
                            7. Validation Checks
```

## 🔧 Environment Variables (Quick Copy)

```yaml
# Essential Variables
ANSIBLE_HOST_KEY_CHECKING: "False"
HOMELAB_ADMIN_USER: "admin"
DISCOVERY_NETWORKS: "['192.168.1.0/24']"
GRAFANA_PORT: "3000"
PROMETHEUS_PORT: "9090"
BACKUP_SCHEDULE: "0 2 * * *"
```

## 🔐 Required Secrets

```yaml
SSH_PRIVATE_KEY: "Your SSH private key"
BACKUP_PASSWORD: "Strong encryption password"
GRAFANA_ADMIN_PASSWORD: "Grafana admin password"
```

## 📊 Inventory Template

```ini
[local]
localhost ansible_connection=local

[homelab:children]
webservers
databases
monitoring
docker_hosts

[webservers]
[databases]
[monitoring]
[docker_hosts]
```

## ⚡ Quick Commands

**Test Discovery:**

```bash
# From Semaphore, run "Inventory Discovery" template
```

**Manual Validation:**

```bash
ansible-playbook -i inventory/discovered-hosts.yml playbooks/validation-checks.yml
```

**Access Services:**

- Grafana: `http://your-host:3000` (admin/your-password)
- Prometheus: `http://your-host:9090`
- Node Exporter: `http://your-host:9100/metrics`

## 🎯 Success Indicators

- ✅ Inventory Discovery finds your hosts
- ✅ Security templates run without errors
- ✅ Monitoring services are accessible
- ✅ Validation checks pass
- ✅ Backup scripts are created and functional

## 🚨 Troubleshooting Quick Fixes

**Can't connect to hosts:**

- Check SSH key in Semaphore Key Store
- Verify host SSH access manually
- Check firewall rules

**Service deployment fails:**

- Verify sudo/root access
- Check disk space (`df -h`)
- Review service logs in Semaphore

**Monitoring not accessible:**

- Check firewall: `ufw status`
- Verify services: `systemctl status prometheus grafana-server`
- Check ports: `netstat -tlnp | grep :3000`

## 📞 Emergency Commands

```bash
# Check service status
systemctl status prometheus grafana-server docker

# Restart services
systemctl restart prometheus grafana-server

# Check firewall
ufw status verbose

# View logs
journalctl -u prometheus -f
journalctl -u grafana-server -f
```

---

**🎉 You're ready to deploy! Start with "Inventory Discovery" template in Semaphore.**
