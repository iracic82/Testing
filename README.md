# Infoblox Automated Workflow for Discovery and Onboarding Cloud Azure Account

This **template repository** provides a **one-click solution** to automate Azure permissions for Infoblox integration.

## 👥 For Customers

**First time using this?** See [CUSTOMER_SETUP.md](CUSTOMER_SETUP.md) for 5-minute setup guide.

**Ready to use?** See [QUICK_START.md](QUICK_START.md) for usage instructions.

## 🏢 For Vendors

**Sharing with customers?** See [VENDOR_GUIDE.md](VENDOR_GUIDE.md) for deployment model.

---

## Overview

This workflow automates the discovery and onboarding of Azure accounts into Infoblox.
Simply enter your **Infoblox Application ID**, and the workflow will automatically configure all Azure permissions.

---

## 🚀 **Deploy to Azure**
<table>
  <tr>
    <td><img src="https://upload.wikimedia.org/wikipedia/commons/a/a8/Microsoft_Azure_Logo.svg" width="120"></td>
    <td>
      <a href="https://github.com/iracic82/Azure_Discovery/actions/workflows/azure-onboard.yml">
        <img src="https://img.shields.io/badge/Deploy%20to%20Azure-Click%20to%20Run-blue?style=for-the-badge&logo=azure">
      </a>
    </td>
  </tr>
</table>

---

## **✅ How It Works** - Two Modes Supported

This workflow supports both **Single** and **Auto-Discover Multiple** modes from Infoblox:

### Mode 1: Auto-Discover Multiple (Default - Recommended)

Configures **ALL subscriptions** in your Azure tenant automatically:

1️⃣ **In Infoblox Portal**:
   - Navigate to Configure → Networking → Discovery → Cloud → Create → Azure
   - Click **"Create Application"**
   - Copy the **Application ID**

2️⃣ **Click the "Deploy to Azure" button**:
   - Paste the **Application ID**
   - **Leave Subscription ID empty** (for auto-discover mode)
   - Click "Run workflow"

3️⃣ **The workflow automatically executes**:
   - ✅ Discovers **ALL subscriptions** in your tenant
   - ✅ Auto-detects **Tenant ID**
   - ✅ Creates service principal: `az ad sp create --id <app-id>`
   - ✅ **For each subscription**, assigns:
     - **Reader** role (for IPAM)
     - **DNS Zone Contributor** role (for public DNS)
     - **Private DNS Zone Contributor** role (for private DNS)
     - **Custom Cloud Forwarding Role** (optional)

4️⃣ **In Infoblox Portal**:
   - Set **Account Preference** to: **Auto-Discover Multiple**
   - Copy and paste the **Tenant ID** from workflow output
   - Infoblox will auto-discover all configured subscriptions

---

### Mode 2: Single Subscription

Configures **ONE specific subscription** only:

1️⃣ **In Infoblox Portal**:
   - Navigate to Configure → Networking → Discovery → Cloud → Create → Azure
   - Click **"Create Application"**
   - Copy the **Application ID**

2️⃣ **Click the "Deploy to Azure" button**:
   - Paste the **Application ID**
   - **Enter your Subscription ID** (for single mode)
   - Click "Run workflow"

3️⃣ **The workflow executes for the specific subscription**:
   - ✅ Configures only the specified subscription
   - ✅ Auto-detects **Tenant ID**
   - ✅ Creates service principal: `az ad sp create --id <app-id>`
   - ✅ Assigns all required roles to the single subscription

4️⃣ **In Infoblox Portal**:
   - Set **Account Preference** to: **Single**
   - Copy and paste the **Subscription ID** from workflow output
   - Copy and paste the **Tenant ID** from workflow output

---

## 📋 **Prerequisites**

### 1. Get Your Infoblox Application ID
From the Infoblox Portal:
- Navigate to **Configure → Networking → Discovery**
- Click **Cloud → Create → Azure**
- Copy the **Application ID** displayed

### 2. Configure GitHub Secrets
You need to set up Azure credentials as a GitHub secret:

1. Create an Azure Service Principal for GitHub Actions:
```bash
az ad sp create-for-rbac --name "github-actions-infoblox" \
  --role "Owner" \
  --scopes /subscriptions/{subscription-id} \
  --sdk-auth
```

2. Copy the JSON output and add it as a secret named `AZURE_CREDENTIALS` in your GitHub repository:
   - Go to **Settings → Secrets and variables → Actions → New repository secret**
   - Name: `AZURE_CREDENTIALS`
   - Value: Paste the JSON output

---

## 🔐 **Permissions Assigned**

The workflow assigns the following Azure roles as per Infoblox documentation:

### Built-in Roles:
- ✅ **Reader** - For IPAM synchronization and asset discovery
- ✅ **DNS Zone Contributor** - For managing Azure DNS zones and records
- ✅ **Private DNS Zone Contributor** - For managing Private DNS zones and records

### Custom Role (Optional):
- ✅ **Infoblox Cloud Forwarding Custom Role** - For Cloud Forwarding with:
  - Write and delete permissions for resource groups
  - DNS resolver management
  - DNS forwarding ruleset management
  - Virtual network and subnet access

---

## 🔧 **What Gets Configured**

The automated workflow (aligned with Infoblox documentation):

1. **Mode Selection**:
   - **Auto-Discover Multiple**: Automatically detects and configures **ALL subscriptions** in your tenant
   - **Single**: Configures **ONE specific subscription** that you specify
   - Skips disabled subscriptions automatically

2. **Service Principal**: Creates the service principal using your Infoblox Application ID
   - Equivalent to: `az ad sp create --id <infoblox-app-id>`

3. **Role Assignments** (for each targeted subscription):
   - **Reader** (for IPAM synchronization)
   - **DNS Zone Contributor** (for public DNS management)
   - **Private DNS Zone Contributor** (for private DNS management)
   - **Custom Cloud Forwarding Role** (for advanced DNS forwarding features)

4. **Summary Report**:
   - **🎯 Displays Tenant ID** ← You copy this to Infoblox Portal
   - **🎯 Displays Subscription ID** (in Single mode)
   - Lists all configured subscriptions
   - Shows which roles were assigned to each subscription

---

## 📤 **Final Output**

After the workflow completes, you'll see a summary. The format depends on which mode you used:

### Auto-Discover Multiple Mode Output:

```
╔══════════════════════════════════════════════════════════════════╗
║        Azure Configuration Summary for Infoblox                  ║
║              Auto-Discover Multiple Mode                         ║
╚══════════════════════════════════════════════════════════════════╝

🎯 COPY THESE VALUES TO INFOBLOX PORTAL:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Tenant ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Next Steps in Infoblox Portal:
1. Set Account Preference to: Auto-Discover Multiple
2. Paste the Tenant ID shown above
3. The system will auto-discover all configured subscriptions
```

### Single Mode Output:

```
╔══════════════════════════════════════════════════════════════════╗
║        Azure Configuration Summary for Infoblox                  ║
║                  Single Subscription Mode                        ║
╚══════════════════════════════════════════════════════════════════╝

🎯 COPY THESE VALUES TO INFOBLOX PORTAL:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Tenant ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
  Subscription ID: yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Next Steps in Infoblox Portal:
1. Set Account Preference to: Single
2. Paste the Subscription ID shown above
3. Paste the Tenant ID shown above
```

---

## 📖 **Manual Setup (Alternative)**

If you prefer to configure manually, follow the [Infoblox Azure Setup Guide](https://docs.infoblox.com/) which covers:
- Creating the application in Azure AD
- Configuring Reader role for IPAM synchronization
- Setting up DNS Zone Contributor permissions
- Creating custom roles for Cloud Forwarding  



