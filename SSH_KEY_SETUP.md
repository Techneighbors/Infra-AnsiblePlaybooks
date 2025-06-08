# 🔑 SSH Key Setup for Semaphore

## Your Existing SSH Keys

✅ **You already have SSH keys!**

- **Private Key**: `path to key`
- **Public Key**: `path to key
- **Key Type**: Ed25519 (modern and secure!)

## 🔐 Step 1: Copy Private Key for Semaphore

**Copy this ENTIRE private key content to Semaphore Key Store:**

```
-----BEGIN OPENSSH PRIVATE KEY-----
KEY HERE
-----END OPENSSH PRIVATE KEY-----
```

## 📋 Step 2: Add to Semaphore Key Store

1. **Login to Semaphore UI**
2. **Go to Project Settings → Key Store**
3. **Click "New Key"**
4. **Configure**:
   - **Name**: `Homelab-SSH-Key`
   - **Type**: `SSH`
   - **Private Key**: Paste the private key above (including BEGIN/END lines)
   - **Passphrase**: Leave empty (your key doesn't have one)

## 🏠 Step 3: Ensure Public Key is on Homelab Hosts

Your **public key** needs to be in the `~/.ssh/authorized_keys` file on each homelab host:

### Option A: Copy Key to Host (Manual)

```bash
# From your Windows machine to each Linux host
ssh-copy-id admin@192.168.1.10
ssh-copy-id admin@192.168.1.11
# ... repeat for each host
```

### Option B: Manual Installation on Each Host

1. **SSH into each host**:

   ```bash
   ssh admin@192.168.1.10
   ```

2. **Create .ssh directory** (if it doesn't exist):

   ```bash
   mkdir -p ~/.ssh
   chmod 700 ~/.ssh
   ```

3. **Add your public key**:
   ```bash
   echo "ssh-ed25519 " >> ~/.ssh/authorized_keys
   chmod 600 ~/.ssh/authorized_keys
   ```

### Option C: Use Ansible (Recommended)

Create a quick playbook to distribute your key:

```yaml
# setup-ssh-keys.yml
---
- name: Setup SSH keys on homelab hosts
  hosts: all
  tasks:
    - name: Add public key to authorized_keys
      ansible.posix.authorized_key:
        user: "{{ ansible_user }}"
        key: ""
        state: present
```

Run it once manually:

```bash
ansible-playbook -i inventory/example-hosts.yml setup-ssh-keys.yml --ask-pass
```

## ✅ Step 4: Test SSH Access

**Test from your Windows machine**:

```bash
ssh admin@192.168.1.10
```

**Test from Semaphore**:

- Create a simple template with a `ping` task
- Run it against your hosts
- Should connect without password prompts

## 🔧 Troubleshooting

**If SSH connection fails:**

1. **Check SSH service on host**:

   ```bash
   sudo systemctl status ssh
   ```

2. **Check SSH logs**:

   ```bash
   sudo tail -f /var/log/auth.log
   ```

3. **Verify key permissions**:

   ```bash
   ls -la ~/.ssh/
   # authorized_keys should be 600
   # .ssh directory should be 700
   ```

4. **Test verbose SSH**:
   ```bash
   ssh -v admin@192.168.1.10
   ```

## 🎯 Expected Result

After setup:

- ✅ SSH from Windows to homelab hosts works without password
- ✅ Semaphore can connect to all hosts using the stored private key
- ✅ Ansible playbooks run successfully through Semaphore
- ✅ Dynamic inventory discovery works automatically

## 🔐 Security Notes

- ✅ **Ed25519 keys are excellent** - modern, fast, secure
- ✅ **No passphrase needed** for automation
- 🔒 **Private key stays secure** in Semaphore's encrypted key store
- 🔒 **Public key is safe** to distribute to all hosts
- 🔒 **Regular key rotation** recommended every 1-2 years

---

**Your SSH setup is ready for Semaphore! 🚀**
