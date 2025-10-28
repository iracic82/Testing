# Mode Comparison: Single vs Auto-Discover Multiple

This document explains the two modes supported by the workflow and when to use each.

## Quick Reference

| Feature | Single Mode | Auto-Discover Multiple Mode |
|---------|-------------|----------------------------|
| **Input Required** | Application ID + Subscription ID | Application ID only |
| **Subscriptions Configured** | 1 specific subscription | ALL subscriptions in tenant |
| **Output** | Tenant ID + Subscription ID | Tenant ID only |
| **Infoblox Setting** | Account Preference: Single | Account Preference: Auto-Discover Multiple |
| **Use Case** | Specific subscription only | All subscriptions in tenant |
| **Recommended For** | Testing, single-subscription tenants | Production, multi-subscription tenants |

---

## Mode 1: Single Subscription

### When to Use:
- ✅ You only want to configure **one specific subscription**
- ✅ You're testing the workflow before rolling out to all subscriptions
- ✅ Your organization only has one subscription
- ✅ You want granular control over which subscription is configured

### How to Use:

**Step 1**: In GitHub Actions workflow:
```
Infoblox Application ID: c2b8300c-4117-48ac-b1d1-3547079b6ed7
Subscription ID: 12345678-1234-1234-1234-123456789012
```

**Step 2**: Workflow configures only that subscription

**Step 3**: In Infoblox Portal:
```
Account Preference: Single
Subscription ID: 12345678-1234-1234-1234-123456789012
Tenant ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

### Output Example:

```
╔══════════════════════════════════════════════════════════════════╗
║        Azure Configuration Summary for Infoblox                  ║
║                  Single Subscription Mode                        ║
╚══════════════════════════════════════════════════════════════════╝

🎯 COPY THESE VALUES TO INFOBLOX PORTAL:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Tenant ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
  Subscription ID: 12345678-1234-1234-1234-123456789012

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Configured Subscriptions (1 total):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  📋 Subscription: Production
     ID: 12345678-1234-1234-1234-123456789012
     State: Enabled

     Roles Assigned:
      ✓ Reader
      ✓ DNS Zone Contributor
      ✓ Private DNS Zone Contributor

     Custom Role for Cloud Forwarding:
      ✓ Infoblox Cloud Forwarding Custom Role

Next Steps in Infoblox Portal:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Set Account Preference to: Single
2. Paste the Subscription ID: 12345678-1234-1234-1234-123456789012
3. Paste the Tenant ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
4. Complete the configuration and test the connection
```

---

## Mode 2: Auto-Discover Multiple (Recommended)

### When to Use:
- ✅ You want to configure **all subscriptions** in your tenant automatically
- ✅ Your organization has multiple subscriptions
- ✅ You want Infoblox to discover all Azure resources across all subscriptions
- ✅ You want to save time and avoid manual configuration for each subscription

### How to Use:

**Step 1**: In GitHub Actions workflow:
```
Infoblox Application ID: c2b8300c-4117-48ac-b1d1-3547079b6ed7
Subscription ID: (leave empty)
```

**Step 2**: Workflow discovers and configures ALL subscriptions

**Step 3**: In Infoblox Portal:
```
Account Preference: Auto-Discover Multiple
Tenant ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

### Output Example:

```
╔══════════════════════════════════════════════════════════════════╗
║        Azure Configuration Summary for Infoblox                  ║
║              Auto-Discover Multiple Mode                         ║
╚══════════════════════════════════════════════════════════════════╝

🎯 COPY THESE VALUES TO INFOBLOX PORTAL:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Tenant ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Configured Subscriptions (3 total):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  📋 Subscription: Production
     ID: 11111111-1111-1111-1111-111111111111
     State: Enabled
     Roles Assigned:
      ✓ Reader
      ✓ DNS Zone Contributor
      ✓ Private DNS Zone Contributor
     Custom Role for Cloud Forwarding:
      ✓ Infoblox Cloud Forwarding Custom Role

  📋 Subscription: Development
     ID: 22222222-2222-2222-2222-222222222222
     State: Enabled
     Roles Assigned:
      ✓ Reader
      ✓ DNS Zone Contributor
      ✓ Private DNS Zone Contributor
     Custom Role for Cloud Forwarding:
      ✓ Infoblox Cloud Forwarding Custom Role

  📋 Subscription: Testing
     ID: 33333333-3333-3333-3333-333333333333
     State: Enabled
     Roles Assigned:
      ✓ Reader
      ✓ DNS Zone Contributor
      ✓ Private DNS Zone Contributor
     Custom Role for Cloud Forwarding:
      ✓ Infoblox Cloud Forwarding Custom Role

Next Steps in Infoblox Portal:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Set Account Preference to: Auto-Discover Multiple
2. Paste the Tenant ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
3. The system will auto-discover all 3 configured subscriptions
4. Complete the configuration and test the connection
```

---

## Comparison Table

| Aspect | Single | Auto-Discover Multiple |
|--------|--------|----------------------|
| **Number of Subscriptions** | 1 | All in tenant |
| **GitHub Input Fields** | App ID + Subscription ID | App ID only |
| **Infoblox Input Fields** | Subscription ID + Tenant ID | Tenant ID only |
| **Discovery Time** | Fast (1 subscription) | Slower (multiple subscriptions) |
| **Flexibility** | Choose specific subscription | Automatic for all |
| **Maintenance** | Manual per subscription | Automatic |
| **Best For** | Testing, single-sub tenants | Production, multi-sub tenants |

---

## Switching Between Modes

### From Single to Auto-Discover Multiple:

1. Run the workflow again with **Subscription ID empty**
2. The workflow will configure all other subscriptions
3. In Infoblox Portal, change **Account Preference** to **Auto-Discover Multiple**
4. Paste only the **Tenant ID**

### From Auto-Discover Multiple to Single:

If you want to limit to just one subscription:
1. In Infoblox Portal, change **Account Preference** to **Single**
2. Enter the specific **Subscription ID** you want to use
3. Enter the **Tenant ID**

Note: The permissions will still exist on all subscriptions from the previous run. You can manually remove them from Azure Portal if needed.

---

## Recommendation

**For most users**: Use **Auto-Discover Multiple** mode
- Automatically configures all subscriptions
- Infoblox discovers all Azure resources across your entire tenant
- Less maintenance when subscriptions are added/removed
- Aligns with Infoblox best practices for enterprise deployments

**Use Single mode only when**:
- Testing the workflow for the first time
- You have a single-subscription tenant
- You explicitly want to exclude certain subscriptions from Infoblox discovery
