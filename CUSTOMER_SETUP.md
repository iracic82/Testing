# Customer Setup Guide

This repository is provided by your vendor to automate Azure permissions for Infoblox integration.

## 🚀 One-Time Setup (5 Minutes)

Follow these steps **once** to set up your own automated workflow:

---

### Step 1: Create Your Own Copy (30 seconds)

1. Go to: **https://github.com/iracic82/Azure_Discovery**
2. Click the green **"Use this template"** button (top right)
3. Click **"Create a new repository"**
4. Give it a name (e.g., `MyCompany-Azure-Infoblox`)
5. Click **"Create repository"**

✅ You now have your own independent copy!

---

### Step 2: Create Azure Service Principal (2 minutes)

Open **Azure Cloud Shell** and run this command:

```bash
az ad sp create-for-rbac \
  --name "github-actions-infoblox" \
  --role "Owner" \
  --scopes /subscriptions/{YOUR-SUBSCRIPTION-ID} \
  --sdk-auth
```

**Replace `{YOUR-SUBSCRIPTION-ID}`** with your actual subscription ID.

📋 **Copy the entire JSON output** - you'll need it in the next step.

---

### Step 3: Add GitHub Secret (1 minute)

1. In your new GitHub repository, go to **Settings** → **Secrets and variables** → **Actions**
2. Click **"New repository secret"**
3. Name: `AZURE_CREDENTIALS`
4. Value: **Paste the JSON from Step 2**
5. Click **"Add secret"**

✅ Setup complete!

---

## 🎯 How to Use

### For Auto-Discover Multiple (All Subscriptions):

1. Get your **Application ID** from Infoblox Portal:
   - Configure → Networking → Discovery → Cloud → Create → Azure
   - Click "Create Application"
   - Copy the Application ID

2. In your GitHub repository:
   - Go to **Actions** tab
   - Click **"Onboard Azure Account for Infoblox DNS"**
   - Click **"Run workflow"**
   - Paste **Application ID**
   - **Leave Subscription ID empty**
   - Click **"Run workflow"**

3. Wait for completion (2-5 minutes)

4. Copy the **Tenant ID** from the output

5. In Infoblox Portal:
   - Set Account Preference: **Auto-Discover Multiple**
   - Paste **Tenant ID**
   - Done!

---

### For Single Subscription:

Same steps as above, but:
- **Enter your Subscription ID** in the workflow
- In Infoblox Portal, set Account Preference to **Single**
- Paste both **Subscription ID** and **Tenant ID**

---

## 🔒 Security Notes

- Your Azure credentials are stored **only in your repository**
- Your vendor **cannot access** your credentials
- The workflow runs **in your own GitHub account**
- All permissions are assigned **to your Azure tenant only**

---

## ❓ Need Help?

- See [README.md](README.md) for detailed documentation
- See [QUICK_START.md](QUICK_START.md) for quick reference
- Contact your vendor for support

---

## 🔄 Updates

Your vendor may release updates to this template. To get updates:

1. Check the original template repository for changes
2. Manually copy any new features to your repository
3. Or recreate from template and re-add your secret

**Note**: Your `AZURE_CREDENTIALS` secret is safe and won't be affected by updates.
