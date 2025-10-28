# Quick Start Guide

Choose your mode and follow the corresponding steps:

## 🚀 Auto-Discover Multiple (Recommended for Most Users)

**Use this when**: You want to configure all subscriptions in your Azure tenant

### Steps:

1. **Infoblox Portal**: Create Application → Copy Application ID
2. **GitHub Actions**:
   - Click "Deploy to Azure" button
   - Paste **Application ID**
   - **Leave Subscription ID EMPTY**
   - Click "Run workflow"
3. **Wait for completion**
4. **Copy Tenant ID** from the output
5. **Infoblox Portal**:
   - Set Account Preference: **Auto-Discover Multiple**
   - Paste **Tenant ID**
   - Done! Infoblox will discover all subscriptions

---

## 🎯 Single Subscription

**Use this when**: You only want to configure one specific subscription

### Steps:

1. **Infoblox Portal**: Create Application → Copy Application ID
2. **GitHub Actions**:
   - Click "Deploy to Azure" button
   - Paste **Application ID**
   - **Enter your Subscription ID**
   - Click "Run workflow"
3. **Wait for completion**
4. **Copy Tenant ID and Subscription ID** from the output
5. **Infoblox Portal**:
   - Set Account Preference: **Single**
   - Paste **Subscription ID**
   - Paste **Tenant ID**
   - Done!

---

## Mode Comparison

| Feature | Single | Auto-Discover Multiple |
|---------|--------|----------------------|
| GitHub Input | App ID + Sub ID | App ID only |
| Infoblox Input | Sub ID + Tenant ID | Tenant ID only |
| Subscriptions Configured | 1 | All in tenant |
| Best For | Testing, 1 subscription | Production, multiple subscriptions |

---

## What Gets Configured

Both modes configure the same permissions per subscription:

✅ **Service Principal** created for Infoblox Application
✅ **Reader** role (for IPAM synchronization)
✅ **DNS Zone Contributor** role (for public DNS management)
✅ **Private DNS Zone Contributor** role (for private DNS management)
✅ **Custom Cloud Forwarding Role** (for advanced DNS features)

---

## Troubleshooting

### Workflow fails with "Subscription not found"
- **Single mode**: Check that the Subscription ID is correct and you have access
- **Solution**: Verify the subscription ID in Azure Portal

### I want to switch from Single to Auto-Discover Multiple
- Run the workflow again with **Subscription ID empty**
- In Infoblox Portal, change to **Auto-Discover Multiple** mode

### I want to switch from Auto-Discover Multiple to Single
- In Infoblox Portal, change to **Single** mode
- Enter the specific Subscription ID you want to use
- The permissions are already configured from the previous run

---

## Need Help?

- See [README.md](README.md) for detailed documentation
- See [MODE_COMPARISON.md](MODE_COMPARISON.md) for mode comparison
- See [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) for technical details
- See [WORKFLOW_COMPARISON.md](WORKFLOW_COMPARISON.md) for manual vs automated comparison
