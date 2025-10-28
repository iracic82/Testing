# Workflow Comparison: Manual vs Automated

This document shows how the automated GitHub Actions workflow aligns with the manual Infoblox Azure setup documentation.

## Manual Process (from Infoblox Documentation)

### Step-by-Step Manual Setup:

1. **Infoblox Portal**: Navigate to Configure → Networking → Discovery → Cloud → Create → Azure
2. **Infoblox Portal**: Click "Create Application"
   - Get **Application ID** (e.g., `c2b8300c-4117-48ac-b1d1-3547079b6ed7`)
   - Get **Application Name** (e.g., `infoblox-access-app-az-com-1-de845130`)

3. **Azure CLI**: Create Service Principal
   ```bash
   az ad sp create --id <app-id-by-infoblox>
   ```

4. **Azure Portal**: Azure Subscription → Access Control (IAM) → Add Role Assignment
   - Assign **Reader** role
   - Search for Application Name from Infoblox Portal
   - Select as member
   - Click "Review + Assign"

5. **Azure Portal**: Add DNS Zone Contributor role
   - Same process as step 4
   - Assign **DNS Zone Contributor** role

6. **Azure Portal**: Add Private DNS Zone Contributor role
   - Same process as step 4
   - Assign **Private DNS Zone Contributor** role

7. **Azure Portal** (Optional for Cloud Forwarding): Create Custom Role
   - Create custom role with write/delete permissions for resource groups
   - Assign to the application

8. **Azure Portal**: Get Tenant ID
   - Navigate to Microsoft Entra ID
   - Copy **Tenant ID**

9. **Infoblox Portal**: Paste Tenant ID (Step 13 in documentation)

---

## Automated Process (This GitHub Workflow)

### Simplified Automated Setup (Auto-Discover Multiple):

1. **Infoblox Portal**: Navigate to Configure → Networking → Discovery → Cloud → Create → Azure
2. **Infoblox Portal**: Click "Create Application"
   - Copy **Application ID**

3. **GitHub**: Click "Deploy to Azure" button
   - Paste **Application ID**
   - Click "Run workflow"

4. **Automation runs in Auto-Discover Multiple mode** (equivalent to manual steps 3-8):
   - ✅ Auto-discovers **ALL Subscription IDs** in your tenant
   - ✅ Auto-discovers Tenant ID
   - ✅ Creates Service Principal once (`az ad sp create --id <app-id>`)
   - ✅ **For EACH subscription**:
     - Assigns **Reader** role
     - Assigns **DNS Zone Contributor** role
     - Assigns **Private DNS Zone Contributor** role
     - Creates and assigns **Cloud Forwarding Custom Role**
   - ✅ Outputs summary with Tenant ID and all configured subscriptions

5. **Infoblox Portal**: Copy **Tenant ID** from workflow output and paste in step 13
   - Infoblox will automatically discover all configured subscriptions

---

## Comparison Table

| Step | Manual Process | Automated Workflow |
|------|---------------|-------------------|
| 1 | Create Application in Infoblox Portal | Create Application in Infoblox Portal |
| 2 | Copy Application ID | Copy Application ID |
| 3 | Run `az ad sp create --id <app-id>` in Azure CLI | Paste App ID in GitHub, click "Run workflow" |
| 4 | Navigate to Azure Portal IAM | ✅ Automated |
| 5 | Assign Reader role manually | ✅ Automated |
| 6 | Assign DNS Zone Contributor manually | ✅ Automated |
| 7 | Assign Private DNS Zone Contributor manually | ✅ Automated |
| 8 | Create custom role for Cloud Forwarding | ✅ Automated |
| 9 | Find Tenant ID in Azure Portal | ✅ Automated (displayed in output) |
| 10 | Paste Tenant ID in Infoblox Portal | Copy Tenant ID from output and paste |

---

## Benefits of Automation

✅ **Reduced Steps**: 10 manual steps per subscription → 3 total steps
✅ **Multi-Subscription Support**: Automatically configures ALL subscriptions in your tenant
✅ **No Azure Portal Navigation**: All IAM configuration automated
✅ **No CLI Commands**: No need to run `az ad sp create`
✅ **Automatic Discovery**: All Subscription IDs and Tenant ID auto-detected
✅ **Idempotent**: Can be run multiple times safely
✅ **Audit Trail**: GitHub Actions provides execution logs
✅ **Consistent**: Eliminates human error in role assignments
✅ **Scalable**: Works with 1 or 100+ subscriptions without extra effort

---

## Permissions Alignment

The automated workflow assigns exactly the roles specified in Infoblox documentation:

### For IPAM (IP Address Management):
- ✅ **Reader** role at subscription level

### For DNS Management:
- ✅ **DNS Zone Contributor** - manages public DNS zones
- ✅ **Private DNS Zone Contributor** - manages private DNS zones

### For Cloud Forwarding (Optional):
- ✅ **Custom Role** with permissions:
  - `Microsoft.Resources/subscriptions/resourceGroups/write`
  - `Microsoft.Resources/subscriptions/resourceGroups/delete`
  - `Microsoft.Network/dnsResolvers/*`
  - `Microsoft.Network/dnsForwardingRulesets/*`
  - `Microsoft.Network/virtualNetworks/read`
  - `Microsoft.Network/virtualNetworks/subnets/read`
  - `Microsoft.Network/virtualNetworks/subnets/join/action`

---

## Technical Implementation

The automation uses:
- **Azure Python SDK** (`azure-identity`, `azure-mgmt-authorization`)
- **Microsoft Graph SDK** (`msgraph-sdk`) for service principal creation
- **GitHub Actions** for workflow execution
- **DefaultAzureCredential** for authentication (using GitHub secret)

All operations align with Infoblox best practices documented at:
- Step 10: Creating Azure Client ID + Tenant ID
- Step 11: Configuring permissions in Azure
- Step 12-13: Providing Tenant ID to Infoblox Portal
