# Vendor Guide: Sharing This Repository with Customers

This guide explains how to use this repository as a **template** that customers can easily deploy.

---

## 🎯 Deployment Model: GitHub Template Repository

**How it works:**
1. Your repository serves as a **template** (not a fork)
2. Customers click **"Use this template"** to create their own copy
3. Each customer sets up their own Azure credentials **once**
4. Customers run workflows in their own repository
5. **Zero maintenance** for customers after initial setup

**Benefits:**
- ✅ One template repository (yours) → unlimited customer deployments
- ✅ Customers get their own independent copy (not a fork)
- ✅ No access to customer credentials (they stay in customer's GitHub)
- ✅ Easy updates: customers can recreate from updated template
- ✅ No ongoing work for customers

---

## 📋 Setup Instructions for Vendors

### Step 1: Convert Your Repository to a Template

1. Go to your repository: https://github.com/iracic82/Azure_Discovery
2. Click **Settings**
3. Scroll to **Template repository** section
4. Check ☑️ **"Template repository"**
5. Save

✅ Your repository is now a template!

---

### Step 2: Share with Customers

Provide customers with:

1. **Template Repository Link**: https://github.com/iracic82/Azure_Discovery
2. **Customer Setup Guide**: [CUSTOMER_SETUP.md](CUSTOMER_SETUP.md)
3. **Support contact** (email, Teams, etc.)

#### Example Email to Customers:

```
Subject: Automated Azure Permissions for Infoblox - One-Click Setup

Hi [Customer Name],

We've created an automated solution for configuring Azure permissions for Infoblox.

🚀 One-time setup (5 minutes):
1. Create your copy: https://github.com/iracic82/Azure_Discovery
   - Click "Use this template"
2. Follow the setup guide: [link to CUSTOMER_SETUP.md]
3. Done! You can now run automated configurations anytime.

Benefits:
✅ Configures all Azure subscriptions automatically
✅ No manual Azure Portal work
✅ Runs in your own GitHub account (secure)
✅ Reusable for all future Infoblox integrations

Need help? Contact us at [your support email]

Best regards,
[Your Company]
```

---

## 🔄 How Customers Use It

Once set up, customers simply:

1. Go to **Actions** tab in their repository
2. Click **"Run workflow"**
3. Enter Infoblox **Application ID**
4. Choose mode (Single or Auto-Discover Multiple)
5. Copy **Tenant ID** to Infoblox Portal

**No maintenance, no updates needed!**

---

## 🆕 Releasing Updates

When you improve the template:

1. Update your template repository
2. Notify customers of new features
3. Customers can:
   - **Option A**: Manually copy new files to their repository
   - **Option B**: Create a new copy from template and re-add their secret

**Customer secrets are never affected by updates.**

---

## 📊 Customer Tracking

Since customers create their own repositories from your template, you can see:
- Number of times template was used (GitHub shows this)
- But you **cannot see**:
  - Customer credentials
  - Workflow runs
  - Configuration details

**This is good for security and privacy!**

---

## 🔐 Security Model

```
┌─────────────────────────────────────────────────────────┐
│ Your Template Repository                                │
│ https://github.com/iracic82/Azure_Discovery            │
│                                                         │
│ Contains:                                               │
│ ✅ Workflow code                                        │
│ ✅ Python scripts                                       │
│ ✅ Documentation                                        │
│ ❌ NO customer credentials                             │
└─────────────────────────────────────────────────────────┘
                        │
                        │ Customer clicks
                        │ "Use this template"
                        ↓
┌─────────────────────────────────────────────────────────┐
│ Customer A Repository                                   │
│ https://github.com/customerA/MyCompany-Azure-Infoblox  │
│                                                         │
│ Contains:                                               │
│ ✅ Copy of your template                                │
│ ✅ Their AZURE_CREDENTIALS secret                       │
│ ✅ Their workflow runs                                  │
│                                                         │
│ You CANNOT access: ❌ Their secrets ❌ Their runs       │
└─────────────────────────────────────────────────────────┘
```

---

## 💡 Best Practices

### For Onboarding:

1. **Pre-sales demo**: Show the template in action
2. **Provide video walkthrough**: Record the 5-minute setup
3. **Offer setup assistance**: First-time setup call/meeting
4. **Create FAQ**: Common questions and answers

### For Support:

1. **Template updates**: Announce in release notes
2. **Customer success**: Check-in after first use
3. **Feedback loop**: Improve based on customer input

### For Documentation:

1. Keep **CUSTOMER_SETUP.md** simple (one page)
2. Keep **QUICK_START.md** as reference
3. Keep **README.md** as detailed docs
4. Version your releases (use Git tags)

---

## 📈 Scaling to Many Customers

This model scales effortlessly:

| Customers | Your Work | Customer Work |
|-----------|-----------|---------------|
| 1 | Create template once | 5-min setup once |
| 10 | No additional work | 5-min setup once each |
| 100 | No additional work | 5-min setup once each |
| 1000+ | No additional work | 5-min setup once each |

**Your workload doesn't increase with more customers!**

---

## 🎯 Alternative: Direct Deployment (Not Recommended)

If customers don't want to use GitHub:

1. Package as **Azure DevOps Pipeline**
2. Package as **standalone script** (less secure)
3. Offer **managed service** (you run it for them)

**But GitHub Template is the most intelligent solution because:**
- ✅ Zero ongoing work for customers
- ✅ Secure (credentials stay with customer)
- ✅ Auditable (workflow runs are logged)
- ✅ Reusable (customers can run unlimited times)
- ✅ Scalable (works for 1 or 1000+ customers)

---

## ❓ FAQ

### Can customers modify the workflow?
Yes! It's their copy. They can customize it for their needs.

### Will customer changes affect the template?
No. Changes in customer repositories don't affect your template.

### Can I update customer repositories?
No. You can only update your template. Customers choose when/if to adopt updates.

### How do I know if customers are using it?
GitHub shows "used by X repositories" on template pages (if repositories are public).

### What if a customer loses their secret?
They recreate the Azure service principal and update the GitHub secret.

---

## 🏆 Success Metrics

Track template success:
- Number of template uses (GitHub shows this)
- Customer satisfaction scores
- Support ticket reduction
- Time saved (vs manual configuration)

---

## 🚀 Next Steps

1. ✅ Convert repository to template (see Step 1 above)
2. ✅ Test the customer flow yourself
3. ✅ Prepare customer communication (email, docs)
4. ✅ Create demo video (optional but recommended)
5. ✅ Start sharing with customers!

**Need help?** Review [CUSTOMER_SETUP.md](CUSTOMER_SETUP.md) from the customer's perspective.
