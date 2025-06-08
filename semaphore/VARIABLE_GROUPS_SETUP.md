# 🔧 Variable Groups Setup for Semaphore v2.11.x

Variable Groups replaced Environment Variables in newer Semaphore versions and use JSON format.

## 📋 Step 1: Create Variable Groups

### 1.1 Production Variables Group

1. **Go to Project → Variable Groups**
2. **Click "New Variable Group"**
3. **Configure**:
   - **Name**: `Homelab Production Variables`
   - **Description**: `Production environment variables for homelab infrastructure`
   - **Variables**: Copy from `semaphore/variable-groups.json`

### 1.2 Secrets Variable Group

1. **Create another Variable Group**
2. **Configure**:
   - **Name**: `Homelab Secrets`
   - **Description**: `Encrypted secrets for homelab infrastructure`
   - **Variables**: Copy from `semaphore/variable-groups-secrets.json`
   - **⚠️ IMPORTANT**: Mark all variables in this group as **SECRET/ENCRYPTED**

## 📝 Step 2: Copy JSON Variables

### Production Variables (copy this JSON):

```json
{
  "ANSIBLE_HOST_KEY_CHECKING": "False",
  "ANSIBLE_TIMEOUT": "30",
  "ANSIBLE_GATHERING": "smart",
  "ANSIBLE_STDOUT_CALLBACK": "yaml",
  "HOMELAB_ADMIN_USER": "admin",
  "HOMELAB_SSH_PORT": "22",
  "HOMELAB_TIMEZONE": "America/New_York",
  "SSH_ROOT_LOGIN": "no",
  "SSH_PASSWORD_AUTHENTICATION": "no",
  "SSH_MAX_TRIES": "3",
  "DOCKER_PRIVILEGED_USERS": "[\"admin\", \"ubuntu\", \"user\"]",
  "COMPOSE_VERSION": "2.24.5",
  "BACKUP_SERVICE_USER": "backup",
  "BACKUP_REPOSITORY": "/backup/restic-repo",
  "BACKUP_SCHEDULE": "0 2 * * *",
  "BACKUP_KEEP_POLICY": "--keep-daily 7 --keep-weekly 4 --keep-monthly 6",
  "PROMETHEUS_VERSION": "2.48.1",
  "GRAFANA_VERSION": "10.2.3",
  "GRAFANA_PORT": "3000",
  "PROMETHEUS_PORT": "9090",
  "NODE_EXPORTER_PORT": "9100",
  "DISCOVERY_NETWORKS": "[\"192.168.1.0/24\", \"10.2.10.0/24\"]",
  "DISCOVERY_TIMEOUT": "3",
  "DISCOVERY_MAX_WORKERS": "50",
  "NOTIFICATION_EMAIL": "admin@homelab.local",
  "SMTP_SERVER": "localhost",
  "SMTP_PORT": "587",
  "SEMAPHORE_PROJECT_NAME": "Homelab Infrastructure"
}
```

### Secrets Variables (copy this JSON and update values):

```json
{
  "GRAFANA_ADMIN_PASSWORD": "your-secure-grafana-password",
  "BACKUP_PASSWORD": "your-secure-backup-encryption-password",
  "MYSQL_ROOT_PASSWORD": "your-secure-mysql-root-password",
  "POSTGRES_PASSWORD": "your-secure-postgres-password"
}
```

## 🎯 Step 3: Assign Variable Groups to Templates

When creating templates:

1. **In Template form**
2. **Variable Groups section**: Select both:

   - ✅ `Homelab Production Variables`
   - ✅ `Homelab Secrets`

3. **Extra Variables** (template-specific):

**Security Hardening Template:**

```json
{
  "ssh_port": 22,
  "ssh_permit_root_login": "no",
  "ssh_password_auth": "no",
  "firewall_allowed_ports": ["22/tcp", "80/tcp", "443/tcp"]
}
```

**Docker Setup Template:**

```json
{
  "docker_privileged_users": ["admin", "ubuntu", "rockhelljumper"],
  "compose_version": "2.24.5"
}
```

**Monitoring Stack Template:**

```json
{
  "grafana_port": 3000,
  "prometheus_port": 9090,
  "grafana_admin_password": "{{ GRAFANA_ADMIN_PASSWORD }}"
}
```

## 🔑 Step 4: Update Your Values

**Important**: Replace these placeholder values with your actual values:

### In Secrets Variable Group:

- **GRAFANA_ADMIN_PASSWORD**: Your chosen Grafana admin password
- **BACKUP_PASSWORD**: Strong encryption password for backups
- **Other passwords**: Set secure passwords for any services you'll use

### In Production Variables:

- **DISCOVERY_NETWORKS**: Update with your actual network ranges
  - Replace `"192.168.1.0/24"` with your home network
  - Replace `"10.2.10.0/24"` with your lab network
- **NOTIFICATION_EMAIL**: Your actual email address
- **HOMELAB_TIMEZONE**: Your actual timezone

## ✅ Step 5: Test Variable Groups

### Create Test Template:

**Template Configuration:**

- **Name**: `Variable Test`
- **Playbook**: `playbooks/validation-checks.yml`
- **Inventory**: `localhost`
- **Variable Groups**: Select both groups
- **Extra Variables**:

```json
{
  "test_mode": true,
  "debug_variables": true
}
```

### Run Test:

1. **Execute the template**
2. **Check logs** for variable values
3. **Verify** variables are being passed correctly

## 🚨 Troubleshooting

### Variables Not Working:

- **Check JSON syntax** (no trailing commas, proper quotes)
- **Verify Variable Groups** are selected in template
- **Test with simple variables** first

### JSON Format Issues:

- **Use JSON validator** online to check syntax
- **Arrays must use brackets**: `["item1", "item2"]`
- **Strings must be quoted**: `"value"`
- **No comments allowed** in JSON

### Secret Variables Not Hidden:

- **Mark variables as SECRET** in Variable Group settings
- **Check permissions** on Variable Group
- **Verify encryption** is enabled

## 📋 Quick Reference

### JSON Array Format:

```json
"DOCKER_PRIVILEGED_USERS": "[\"admin\", \"ubuntu\"]"
```

### JSON String Format:

```json
"GRAFANA_PORT": "3000"
```

### Template Variable Reference:

```yaml
grafana_admin_password: "{{ GRAFANA_ADMIN_PASSWORD }}"
```

---

**Your Variable Groups are ready for Semaphore v2.11.x! 🎉**
