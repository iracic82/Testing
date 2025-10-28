# How to Enable Template Repository

Follow these steps to convert this repository into a GitHub Template that customers can use:

## Steps:

1. **Go to your repository on GitHub**:
   https://github.com/iracic82/Azure_Discovery

2. **Click Settings** (top navigation bar)

3. **Scroll down to the "Template repository" section**

4. **Check the box** ☑️ next to "Template repository"

5. **Done!** The repository is now a template.

---

## What Changes After Enabling Template?

### Before (Regular Repository):
- Users can only **fork** your repository
- Forks maintain connection to your repository
- Harder for customers to customize

### After (Template Repository):
- Users see a green **"Use this template"** button
- Creates a **clean copy** (not a fork)
- No connection to your repository
- Perfect for customers to deploy independently

---

## How Customers Will Use It:

1. They visit: https://github.com/iracic82/Azure_Discovery
2. They click the green **"Use this template"** button
3. They name their new repository (e.g., `MyCompany-Azure-Infoblox`)
4. They get a **complete copy** in their own GitHub account
5. They follow [CUSTOMER_SETUP.md](CUSTOMER_SETUP.md) to configure it

---

## Visual Guide:

```
Your Repository (Template)
https://github.com/iracic82/Azure_Discovery

┌─────────────────────────────────────────┐
│  Azure_Discovery                        │
│                                         │
│  [Use this template ▼]  [Code ▼]       │  ← Green button appears
│                                         │
└─────────────────────────────────────────┘

Customer clicks "Use this template"
                ↓
                ↓
                ↓

Customer's New Repository
https://github.com/customer-name/MyCompany-Azure-Infoblox

┌─────────────────────────────────────────┐
│  MyCompany-Azure-Infoblox               │
│                                         │
│  Complete copy of your template         │
│  Independent from your repository       │
│  Customer can customize freely          │
└─────────────────────────────────────────┘
```

---

## After Enabling Template:

1. **Test it yourself**:
   - Open an incognito/private browser window
   - Go to your repository
   - Verify the "Use this template" button appears

2. **Share with first customer**:
   - Send them the repository link
   - Send them [CUSTOMER_SETUP.md](CUSTOMER_SETUP.md)
   - Offer to help with first setup

3. **Scale to more customers**:
   - Same link works for everyone
   - No additional work needed from you
   - Each customer gets independent copy

---

## Need to Undo?

If you ever need to disable the template:
1. Go to Settings
2. Uncheck "Template repository"
3. Repository returns to normal mode

**Note**: This won't affect existing customer repositories created from the template.

---

## Ready?

✅ Enable template mode (follow steps above)
✅ Push the latest changes (already done)
✅ Start sharing with customers!

The most intelligent solution for vendors sharing with multiple customers! 🚀
