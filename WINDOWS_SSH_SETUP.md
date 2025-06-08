# 🔑 Windows SSH Key Setup for Homelab

## 🚫 Windows Doesn't Have `ssh-copy-id`

You're right! Windows PowerShell doesn't include `ssh-copy-id`. Here are Windows-friendly alternatives:

## 🔧 Method 1: PowerShell SSH Key Copy (Recommended)

### Step 1: Create PowerShell Script

```powershell
# Save this as: copy-ssh-key.ps1
param(
    [Parameter(Mandatory=$true)]
    [string]$HostIP,

    [Parameter(Mandatory=$true)]
    [string]$Username,

    [string]$PublicKeyPath = "$env:USERPROFILE\.ssh\id_rsa.pub"
)

# Read the public key
$publicKey = Get-Content $PublicKeyPath -Raw

# Copy key to remote host
$command = @"
mkdir -p ~/.ssh &&
chmod 700 ~/.ssh &&
echo '$publicKey' >> ~/.ssh/authorized_keys &&
chmod 600 ~/.ssh/authorized_keys &&
echo 'SSH key added successfully!'
"@

Write-Host "Copying SSH key to $Username@$HostIP..." -ForegroundColor Green
ssh $Username@$HostIP $command
```

### Step 2: Use the Script

```powershell
# Save the script above, then run:
.\copy-ssh-key.ps1 -HostIP "192.168.1.10" -Username "rockhelljumper"
.\copy-ssh-key.ps1 -HostIP "192.168.1.11" -Username "admin"
# Repeat for each host
```

## 🔧 Method 2: Manual SSH Copy (Simple)

For each host, run these commands:

```powershell
# Get your public key content
$pubkey = Get-Content "$env:USERPROFILE\.ssh\id_rsa.pub"

# Copy to each host (you'll be prompted for password)
ssh rockhelljumper@192.168.1.10 "mkdir -p ~/.ssh && echo '$pubkey' >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys && chmod 700 ~/.ssh"

# Test passwordless login
ssh rockhelljumper@192.168.1.10
```

## 🔧 Method 3: SCP Method (Alternative)

```powershell
# Copy the public key file to the host
scp "$env:USERPROFILE\.ssh\id_rsa.pub" rockhelljumper@192.168.1.10:~/temp_key.pub

# SSH in and install it
ssh rockhelljumper@192.168.1.10
# Then on the remote host:
mkdir -p ~/.ssh
cat ~/temp_key.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
chmod 700 ~/.ssh
rm ~/temp_key.pub
exit
```

## 🔧 Method 4: One-Liner for Each Host

Replace the IP and username for each host:

```powershell
# For rockhelljumper@192.168.1.10
ssh rockhelljumper@192.168.1.10 "mkdir -p ~/.ssh && echo 'Key Information Here' >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys && chmod 700 ~/.ssh"

# Test it worked
ssh rockhelljumper@192.168.1.10
```

## 📝 Step-by-Step for Your Homelab

### 1. Identify Your Hosts

First, let's list your homelab hosts (update these with your actual IPs and usernames):

```powershell
# Example hosts - update with your actual details
$hosts = @(
    @{IP="IP Address"; User="username"},
    @{IP="IP Address"; User="username"},
    @{IP="IP Address"; User="username"}
    # Add more hosts as needed
)
```

### 2. Copy Key to All Hosts

```powershell
# Your public key
$publicKey = Get-Content "$env:USERPROFILE\.ssh\id_rsa.pub"

# Copy to each host
foreach ($target in $hosts) {
    Write-Host "Setting up SSH key for $($target.User)@$($target.IP)..." -ForegroundColor Green

    $command = "mkdir -p ~/.ssh && echo '$publicKey' >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys && chmod 700 ~/.ssh"

    try {
        ssh "$($target.User)@$($target.IP)" $command
        Write-Host "✅ Success: $($target.User)@$($target.IP)" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Failed: $($target.User)@$($target.IP)" -ForegroundColor Red
    }
}
```

### 3. Test All Connections

```powershell
# Test passwordless SSH to each host
foreach ($target in $hosts) {
    Write-Host "Testing connection to $($target.User)@$($target.IP)..." -ForegroundColor Blue
    ssh "$($target.User)@$($target.IP)" "echo 'SSH connection successful from Windows!'"
}
```

## 🎯 Quick Test Commands

After setting up SSH keys, test each host:

```powershell
# Test individual hosts
ssh rockhelljumper@192.168.1.10 "hostname && whoami"
ssh admin@192.168.1.11 "hostname && whoami"

# Should connect without asking for password!
```

## 🔧 Troubleshooting

### PowerShell Variable Error: "Cannot overwrite variable Host"

**Problem**: Getting error `Cannot overwrite variable Host because it is read-only or constant`

**Solution**: PowerShell has a built-in `$Host` variable. Use different variable names:

```powershell
# ❌ This will fail:
foreach ($host in $hosts) { ... }

# ✅ Use this instead:
foreach ($target in $hosts) { ... }
# or
foreach ($server in $hosts) { ... }
# or
foreach ($hostEntry in $hosts) { ... }
```

### Permission Denied?

```powershell
# Check if the key was added correctly
ssh rockhelljumper@192.168.1.10 "ls -la ~/.ssh/ && cat ~/.ssh/authorized_keys"
```

### Still Asking for Password?

1. **Check SSH service on host**:

   ```bash
   sudo systemctl status ssh
   ```

2. **Verify SSH configuration allows key auth**:

   ```bash
   sudo grep -i "PubkeyAuthentication" /etc/ssh/sshd_config
   # Should show: PubkeyAuthentication yes
   ```

3. **Check SSH logs on host**:
   ```bash
   sudo tail -f /var/log/auth.log
   ```

### Can't Connect at All?

1. **Test basic SSH**:

   ```powershell
   ssh -v rockhelljumper@192.168.1.10
   ```

2. **Check host is reachable**:

   ```powershell
   ping 192.168.1.10
   ```

3. **Verify SSH port**:
   ```powershell
   telnet 192.168.1.10 22
   ```

## ✅ Success Checklist

After running the setup:

- [ ] SSH to each host works without password prompt
- [ ] `ssh user@host "whoami"` returns the username
- [ ] No "Permission denied" errors
- [ ] Ready to add SSH key to Semaphore Key Store

## 🚀 Next Steps

1. **Test all connections** work passwordlessly
2. **Add private key to Semaphore** Key Store (from previous guide)
3. **Create simple Semaphore template** to test connection
4. **Run inventory discovery** to find all your hosts automatically

---

**Windows SSH key setup complete! 🎉**
