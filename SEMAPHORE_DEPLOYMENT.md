# 🚀 Semaphore Deployment Guide

Complete step-by-step guide for deploying your homelab infrastructure through Semaphore.

## 📋 Prerequisites

- Semaphore UI installed and accessible
- Git repository with your Ansible playbooks
- SSH access to your homelab hosts
- Python 3.6+ on target hosts

## 🔧 Step 1: Repository Setup

### 1.1 Push Code to Git Repository

```bash
# Initialize git repository (if not already done)
git init
git add .
git commit -m "Initial homelab infrastructure setup"

# Push to your Git repository
git remote add origin https://github.com/yourusername/Infra-AnsiblePlaybooks.git
git push -u origin main
```

### 1.2 Verify Repository Structure

Ensure your repository has this structure:

```
├── ansible.cfg
├── playbooks/
│   ├── security-hardening.yml
│   ├── docker-setup.yml
│   ├── backup-setup.yml
│   ├── monitoring-setup.yml
│   ├── inventory-management.yml
│   └── validation-checks.yml
├── scripts/
│   ├── dynamic_inventory.py
│   └── homelab-discover
├── config/
│   └── discovery.yml
├── inventory/
│   └── example-hosts.yml
└── semaphore/
    ├── environment-vars.yml
    ├── secrets-template.yml
    └── workflows/
```

## 🏗️ Step 2: Semaphore Project Configuration

### 2.1 Create New Project

1. Login to your Semaphore instance
2. Click **"New Project"**
3. Fill in project details:
   - **Name**: `Homelab Infrastructure`
   - **Description**: `Automated homelab infrastructure management`

### 2.2 Configure Repository

1. Go to **Project Settings → Repositories**
2. Click **"New Repository"**
3. Configure:
   - **Name**: `Homelab-Main`
   - **Git URL**: `https://github.com/yourusername/Infra-AnsiblePlaybooks.git`
   - **Branch**: `main`
   - **Access Key**: Create SSH key or use existing

### 2.3 Setup SSH Access Key

1. Go to **Project Settings → Key Store**
2. Click **"New Key"**
3. Configure:
   - **Name**: `Homelab-SSH-Key`
   - **Type**: `SSH`
   - **Private Key**: Paste your SSH private key
   - **Passphrase**: (if applicable)

## 🔐 Step 3: Variable Groups Configuration (v2.11.x)

### 3.1 Create Production Variable Group

1. Go to **Project Settings → Variable Groups**
2. Click **"New Variable Group"**
3. Configure:
   - **Name**: `Homelab Production Variables`
   - **Description**: `Production environment variables for homelab infrastructure`
   - **Variables**: Copy JSON from `semaphore/variable-groups.json`

### 3.2 Create Secrets Variable Group

1. Create another Variable Group:
   - **Name**: `Homelab Secrets`
   - **Description**: `Encrypted secrets for homelab infrastructure`
   - **Variables**: Copy JSON from `semaphore/variable-groups-secrets.json`
   - **⚠️ IMPORTANT**: Mark all variables in this group as **SECRET/ENCRYPTED**

### 3.3 Essential Variables to Update

**In Production Variables:**

- Update `DISCOVERY_NETWORKS` with your actual network ranges
- Set `NOTIFICATION_EMAIL` to your email address

**In Secrets Variables:**

- Set `GRAFANA_ADMIN_PASSWORD` to your chosen password
- Set `BACKUP_PASSWORD` to a strong encryption password

📋 **See `semaphore/VARIABLE_GROUPS_SETUP.md` for complete setup instructions**

## 📊 Step 4: Inventory Configuration

### 4.1 Create Dynamic Inventory

1. Go to **Project Settings → Inventories**
2. Click **"New Inventory"**
3. Configure:

   - **Name**: `Dynamic Inventory`
   - **User Credentials**: `Homelab-SSH-Key` (select your SSH key)
   - **Type**: `File`
   - **Path to Inventory file**: `inventory/dynamic-hosts.yml`
   - **Repository**: Select your repository

**Note**: The inventory content is stored in the file `inventory/dynamic-hosts.yml` in your Git repository, not pasted into Semaphore. Make sure this file exists in your repository with your actual host configurations.

### 4.2 Create Static Inventory (Fallback)

1. Create another inventory:
   - **Name**: `Static Inventory`
   - **User Credentials**: `Homelab-SSH-Key` (select your SSH key)
   - **Type**: `File`
   - **Path to Inventory file**: `inventory/example-hosts.yml`
   - **Repository**: Select your repository

**Note**: This inventory references the existing `inventory/example-hosts.yml` file in your repository. Update that file with your actual host IPs and names. This serves as a backup when dynamic discovery isn't working.

## 🎯 Step 5: Template Configuration

### 5.1 Inventory Discovery Template

1. Go to **Project Settings → Templates**
2. Click **"New Template"**
3. Configure:
   - **Name**: `Inventory Discovery`
   - **Playbook**: `playbooks/inventory-management.yml`
   - **Inventory**: `Static Inventory`
   - **Repository**: `Homelab-Main`
   - **Variable Groups**: Select both `Homelab Production Variables` and `Homelab Secrets`
   - **Extra Variables** (JSON format):
   ```json
   {
     "auto_update_static": true,
     "backup_old_inventory": true,
     "discovery_networks": ["192.168.1.0/24", "10.2.10.0/24"]
   }
   ```

### 5.2 Security Hardening Template

1. Create new template:
   - **Name**: `Security Hardening`
   - **Playbook**: `playbooks/security-hardening.yml`
   - **Inventory**: `Dynamic Inventory`
   - **Variable Groups**: Select both `Homelab Production Variables` and `Homelab Secrets`
   - **Extra Variables** (JSON format):
   ```json
   {
     "ssh_port": 22,
     "ssh_permit_root_login": "no",
     "ssh_password_auth": "no",
     "firewall_allowed_ports": ["22/tcp", "80/tcp", "443/tcp"]
   }
   ```

### 5.3 Docker Setup Template

1. Create new template:
   - **Name**: `Docker Installation`
   - **Playbook**: `playbooks/docker-setup.yml`
   - **Inventory**: `Dynamic Inventory`
   - **Variable Groups**: Select both `Homelab Production Variables` and `Homelab Secrets`
   - **Host Limit**: `docker_hosts`
   - **Extra Variables** (JSON format):
   ```json
   {
     "docker_privileged_users": ["admin", "ubuntu", "rockhelljumper"],
     "compose_version": "2.24.5"
   }
   ```

### 5.4 Monitoring Stack Template

1. Create new template:
   - **Name**: `Monitoring Stack`
   - **Playbook**: `playbooks/monitoring-setup.yml`
   - **Inventory**: `Dynamic Inventory`
   - **Variable Groups**: Select both `Homelab Production Variables` and `Homelab Secrets`
   - **Extra Variables** (JSON format):
   ```json
   {
     "grafana_admin_password": "{{ GRAFANA_ADMIN_PASSWORD }}",
     "prometheus_port": 9090,
     "grafana_port": 3000,
     "node_exporter_port": 9100
   }
   ```

### 5.5 Complete Infrastructure Template

1. Create new template:
   - **Name**: `Complete Infrastructure`
   - **Playbook**: `playbooks/homelab-complete-setup.yml`
   - **Inventory**: `Dynamic Inventory`
   - **Variable Groups**: Select both `Homelab Production Variables` and `Homelab Secrets`
   - **Extra Variables** (JSON format):
   ```json
   {
     "enable_security": true,
     "enable_docker": true,
     "enable_monitoring": true,
     "enable_backup": true,
     "parallel": false
   }
   ```

## 🔄 Step 6: Deployment Workflow

### 6.1 Manual Deployment Steps

**Phase 1: Discovery**

1. Run `Inventory Discovery` template
2. Verify hosts are discovered correctly
3. Check inventory reports

**Phase 2: Security Foundation**

1. Run `Security Hardening` template
2. Run `System Updates` template
3. Verify firewall and fail2ban status

**Phase 3: Core Services**

1. Run `Docker Installation` template (on docker_hosts)
2. Run `Backup Setup` template
3. Verify services are running

**Phase 4: Monitoring**

1. Run `Monitoring Stack` template
2. Access Grafana at `http://host:3000`
3. Access Prometheus at `http://host:9090`

**Phase 5: Validation**

1. Run `Validation Checks` template
2. Review validation reports
3. Fix any issues found

### 6.2 Automated Workflow (Optional)

Create a **Workflow** in Semaphore:

1. Go to **Workflows**
2. Import from `semaphore/workflows/complete-deployment.yml`
3. Customize stages as needed

## 📈 Step 7: Monitoring and Maintenance

### 7.1 Setup Scheduled Tasks

1. **Daily System Updates**:

   - Template: `System Updates`
   - Schedule: `0 2 * * *` (2 AM daily)

2. **Weekly Security Scans**:

   - Template: `Security Hardening`
   - Schedule: `0 3 * * 0` (3 AM Sunday)

3. **Monthly Full Validation**:
   - Template: `Validation Checks`
   - Schedule: `0 4 1 * *` (4 AM 1st of month)

### 7.2 Configure Notifications

1. Go to **Project Settings → Integrations**
2. Add email/webhook notifications
3. Configure alerts for:
   - Deployment failures
   - Security issues
   - Backup failures

## 🚨 Step 8: Testing and Validation

### 8.1 Initial Test Run

1. Start with `Inventory Discovery`
2. Verify hosts are found
3. Run `Validation Checks` on a test host

### 8.2 Gradual Rollout

1. Test on 1-2 hosts first
2. Validate all services work
3. Gradually expand to all hosts

### 8.3 Rollback Plan

1. Keep backup of working configurations
2. Test rollback procedures
3. Document recovery steps

## 📋 Step 9: Post-Deployment Checklist

- [ ] All hosts discovered and accessible
- [ ] SSH hardening applied
- [ ] Firewall configured and active
- [ ] Docker installed on designated hosts
- [ ] Monitoring stack deployed and accessible
- [ ] Backup solution configured and tested
- [ ] Validation checks passing
- [ ] Scheduled tasks configured
- [ ] Notifications working
- [ ] Documentation updated

## 🔧 Troubleshooting

### Common Issues

**Inventory Discovery Fails**:

- Check network configuration in `config/discovery.yml`
- Verify SSH access to hosts
- Check Python dependencies

**SSH Connection Issues**:

- Verify SSH key in Semaphore key store
- Check firewall rules on target hosts
- Validate SSH user permissions

**Service Deployment Fails**:

- Check system requirements
- Verify sufficient disk space
- Review service logs

**Monitoring Stack Issues**:

- Check port availability
- Verify firewall rules
- Check service dependencies

### Getting Help

1. Check Semaphore logs in the UI
2. Review Ansible playbook output
3. SSH to hosts for manual verification
4. Check service status: `systemctl status <service>`

## 🎉 Success Metrics

Your deployment is successful when:

- ✅ All hosts are discovered automatically
- ✅ Security hardening is applied consistently
- ✅ Services are running and accessible
- ✅ Monitoring dashboards show data
- ✅ Backups are configured and tested
- ✅ Validation checks pass on all hosts
- ✅ Scheduled maintenance is working

## 📚 Next Steps

1. **Expand Services**: Add nginx, databases, media servers
2. **Advanced Monitoring**: Set up alerting rules
3. **Security**: Implement vulnerability scanning
4. **Automation**: Create more sophisticated workflows
5. **Documentation**: Keep runbooks updated

Your homelab infrastructure is now fully automated through Semaphore! 🏠✨
