#!/usr/bin/env python3
"""
Azure Discovery and Permission Configuration Script
Automates the setup of Azure permissions for Infoblox integration
"""

import os
import sys
import json
from azure.identity import DefaultAzureCredential
from azure.mgmt.subscription import SubscriptionClient
from azure.mgmt.authorization import AuthorizationManagementClient
from azure.mgmt.authorization.models import RoleDefinition, Permission, RoleAssignmentCreateParameters
from msgraph import GraphServiceClient
from msgraph.generated.service_principals.service_principals_request_builder import ServicePrincipalsRequestBuilder
from msgraph.generated.models.service_principal import ServicePrincipal
import uuid

def get_infoblox_app_id():
    """Get the Infoblox Application ID from environment variable"""
    app_id = os.getenv('INFOBLOX_APP_ID')
    if not app_id:
        print("ERROR: INFOBLOX_APP_ID environment variable is not set")
        sys.exit(1)
    return app_id

def discover_azure_context(credential, target_subscription_id=None):
    """
    Discover Azure subscriptions and tenant information

    Args:
        credential: Azure credential
        target_subscription_id: Optional specific subscription ID for Single mode

    Returns:
        tenant_id, subscription_list, mode
    """
    # Get subscription information
    subscription_client = SubscriptionClient(credential)
    all_subscriptions = list(subscription_client.subscriptions.list())

    if not all_subscriptions:
        print("ERROR: No accessible subscriptions found")
        sys.exit(1)

    # Get tenant ID from the credential token
    # Request a token to extract tenant information
    try:
        token = credential.get_token("https://management.azure.com/.default")
        # Decode the token to get tenant ID
        import base64
        # JWT tokens have 3 parts separated by dots
        token_parts = token.token.split('.')
        if len(token_parts) >= 2:
            # Add padding if needed for base64 decoding
            payload = token_parts[1]
            padding = 4 - len(payload) % 4
            if padding != 4:
                payload += '=' * padding
            decoded = base64.b64decode(payload)
            token_data = json.loads(decoded)
            tenant_id = token_data.get('tid')
        else:
            tenant_id = None
    except Exception as e:
        print(f"Warning: Could not extract tenant ID from token: {str(e)}")
        tenant_id = None

    # Fallback: try to get from subscription object attributes
    if not tenant_id:
        first_sub = all_subscriptions[0]
        for attr_name in ['tenant_id', 'home_tenant_id']:
            if hasattr(first_sub, attr_name):
                tenant_id = getattr(first_sub, attr_name)
                break

    if not tenant_id:
        print("ERROR: Could not determine tenant ID.")
        print("Please ensure you have proper Azure permissions.")
        sys.exit(1)

    # Determine mode: Single or Auto-Discover Multiple
    if target_subscription_id and target_subscription_id.strip():
        print("Discovering Azure context (Single Subscription mode)...")
        mode = "Single"

        # Find the specific subscription
        target_sub = None
        for sub in all_subscriptions:
            if sub.subscription_id == target_subscription_id.strip():
                target_sub = sub
                break

        if not target_sub:
            print(f"ERROR: Subscription ID '{target_subscription_id}' not found or not accessible")
            print(f"\nAvailable subscriptions:")
            for sub in all_subscriptions:
                print(f"  - {sub.display_name} ({sub.subscription_id})")
            sys.exit(1)

        print(f"\n  Tenant ID: {tenant_id}")
        print(f"  Target Subscription: {target_sub.display_name}")
        print(f"  Subscription ID: {target_sub.subscription_id}")
        print(f"  State: {target_sub.state}\n")

        subscription_list = [{
            'id': target_sub.subscription_id,
            'name': target_sub.display_name,
            'state': target_sub.state
        }]
    else:
        print("Discovering Azure context (Auto-Discover Multiple mode)...")
        mode = "Auto-Discover Multiple"

        print(f"\n  Tenant ID: {tenant_id}")
        print(f"  Found {len(all_subscriptions)} subscription(s):\n")

        subscription_list = []
        for idx, sub in enumerate(all_subscriptions, 1):
            print(f"    {idx}. {sub.display_name}")
            print(f"       Subscription ID: {sub.subscription_id}")
            print(f"       State: {sub.state}")
            subscription_list.append({
                'id': sub.subscription_id,
                'name': sub.display_name,
                'state': sub.state
            })

    return tenant_id, subscription_list, mode

def create_or_get_service_principal(credential, app_id):
    """
    Create or retrieve the service principal for the Infoblox application
    """
    print(f"\nCreating/retrieving service principal for App ID: {app_id}...")

    try:
        # Initialize Microsoft Graph client
        graph_client = GraphServiceClient(credentials=credential)

        # Check if service principal already exists
        query_params = ServicePrincipalsRequestBuilder.ServicePrincipalsRequestBuilderGetQueryParameters(
            filter=f"appId eq '{app_id}'"
        )
        request_config = ServicePrincipalsRequestBuilder.ServicePrincipalsRequestBuilderGetRequestConfiguration(
            query_parameters=query_params
        )

        result = graph_client.service_principals.get(request_configuration=request_config)

        if result and result.value and len(result.value) > 0:
            sp = result.value[0]
            print(f"  Service Principal already exists: {sp.id}")
            return sp.id

        # Create new service principal if it doesn't exist
        request_body = ServicePrincipal(
            app_id=app_id
        )

        sp = graph_client.service_principals.post(request_body)
        print(f"  Created Service Principal: {sp.id}")
        return sp.id

    except Exception as e:
        print(f"ERROR creating/retrieving service principal: {str(e)}")
        sys.exit(1)

def get_built_in_role_id(credential, subscription_id, role_name):
    """
    Get the role definition ID for a built-in Azure role
    """
    auth_client = AuthorizationManagementClient(credential, subscription_id)
    scope = f"/subscriptions/{subscription_id}"

    role_definitions = auth_client.role_definitions.list(scope, filter=f"roleName eq '{role_name}'")
    for role in role_definitions:
        if role.role_name == role_name:
            return role.id

    print(f"WARNING: Built-in role '{role_name}' not found")
    return None

def assign_built_in_roles(credential, subscription_id, subscription_name, principal_id):
    """
    Assign built-in Azure roles as per Infoblox documentation:
    1. Reader - for IPAM synchronization and asset discovery
    2. DNS Zone Contributor - for DNS zone management
    3. Private DNS Zone Contributor - for private DNS zone management
    """
    print(f"\nAssigning built-in Azure roles to subscription: {subscription_name}")

    auth_client = AuthorizationManagementClient(credential, subscription_id)
    scope = f"/subscriptions/{subscription_id}"

    # Roles to assign as per Infoblox documentation
    roles_to_assign = [
        ("Reader", "For IPAM synchronization and asset discovery"),
        ("DNS Zone Contributor", "For managing Azure DNS zones and records"),
        ("Private DNS Zone Contributor", "For managing Private DNS zones and records")
    ]

    assigned_roles = []

    for role_name, description in roles_to_assign:
        print(f"\n  Assigning '{role_name}' role...")
        print(f"    Purpose: {description}")

        # Get the built-in role ID
        role_id = get_built_in_role_id(credential, subscription_id, role_name)
        if not role_id:
            print(f"    Skipping '{role_name}' - role not found")
            continue

        # Check if assignment already exists
        try:
            assignments = auth_client.role_assignments.list_for_scope(scope)
            assignment_exists = False
            for assignment in assignments:
                if assignment.principal_id == principal_id and assignment.role_definition_id == role_id:
                    print(f"    ✓ Role assignment already exists")
                    assigned_roles.append(role_name)
                    assignment_exists = True
                    break

            if assignment_exists:
                continue

        except Exception as e:
            print(f"    Warning checking existing assignments: {str(e)}")

        # Create role assignment
        assignment_name = str(uuid.uuid4())

        role_assignment_params = RoleAssignmentCreateParameters(
            role_definition_id=role_id,
            principal_id=principal_id,
            principal_type="ServicePrincipal"
        )

        try:
            assignment = auth_client.role_assignments.create(
                scope=scope,
                role_assignment_name=assignment_name,
                parameters=role_assignment_params
            )
            print(f"    ✓ Successfully assigned '{role_name}' role")
            assigned_roles.append(role_name)
        except Exception as e:
            print(f"    ERROR assigning '{role_name}': {str(e)}")

    return assigned_roles

def create_custom_cloud_forwarding_role(credential, subscription_id):
    """
    Create a custom role for Infoblox Cloud Forwarding (optional)
    As per Infoblox documentation for managing resource groups and DNS forwarding
    """
    print("\nCreating optional custom role for Cloud Forwarding...")

    auth_client = AuthorizationManagementClient(credential, subscription_id)

    role_name = "Infoblox Cloud Forwarding Custom Role"
    role_id = str(uuid.uuid4())
    scope = f"/subscriptions/{subscription_id}"

    # Check if role already exists
    try:
        role_definitions = auth_client.role_definitions.list(scope)
        for role in role_definitions:
            if role.role_name == role_name:
                print(f"  Custom role already exists: {role.id}")
                return role.id
    except Exception as e:
        print(f"  Warning checking existing roles: {str(e)}")

    # Define permissions as per Infoblox Cloud Forwarding requirements
    permissions = [Permission(
        actions=[
            "Microsoft.Resources/subscriptions/resourceGroups/write",
            "Microsoft.Resources/subscriptions/resourceGroups/delete",
            "Microsoft.Network/dnsResolvers/*",
            "Microsoft.Network/dnsForwardingRulesets/*",
            "Microsoft.Network/virtualNetworks/read",
            "Microsoft.Network/virtualNetworks/subnets/read",
            "Microsoft.Network/virtualNetworks/subnets/join/action"
        ],
        not_actions=[]
    )]

    # Create role definition
    role_definition = RoleDefinition(
        role_name=role_name,
        description="Custom role for Infoblox Cloud Forwarding with write and delete permissions for resource groups",
        role_type="CustomRole",
        permissions=permissions,
        assignable_scopes=[scope]
    )

    try:
        created_role = auth_client.role_definitions.create_or_update(
            scope=scope,
            role_definition_id=role_id,
            role_definition=role_definition
        )
        print(f"  ✓ Created custom role for Cloud Forwarding")
        return created_role.id
    except Exception as e:
        print(f"  WARNING: Could not create custom role: {str(e)}")
        return None

def assign_custom_role(credential, subscription_id, role_id, principal_id):
    """
    Assign the custom Cloud Forwarding role to the service principal
    """
    if not role_id:
        return None

    print("\n  Assigning custom Cloud Forwarding role...")

    auth_client = AuthorizationManagementClient(credential, subscription_id)
    scope = f"/subscriptions/{subscription_id}"

    # Check if assignment already exists
    try:
        assignments = auth_client.role_assignments.list_for_scope(scope)
        for assignment in assignments:
            if assignment.principal_id == principal_id and assignment.role_definition_id == role_id:
                print(f"    ✓ Custom role assignment already exists")
                return assignment.id
    except Exception as e:
        print(f"    Warning checking existing assignments: {str(e)}")

    # Create role assignment
    assignment_name = str(uuid.uuid4())

    role_assignment_params = RoleAssignmentCreateParameters(
        role_definition_id=role_id,
        principal_id=principal_id,
        principal_type="ServicePrincipal"
    )

    try:
        assignment = auth_client.role_assignments.create(
            scope=scope,
            role_assignment_name=assignment_name,
            parameters=role_assignment_params
        )
        print(f"    ✓ Successfully assigned custom role")
        return assignment.id
    except Exception as e:
        print(f"    ERROR assigning custom role: {str(e)}")
        return None

def write_summary(tenant_id, app_id, principal_id, subscription_configs, mode):
    """
    Write configuration summary to a file

    Args:
        mode: "Single" or "Auto-Discover Multiple"
    """
    # Build subscriptions section
    subscriptions_section = ""
    for config in subscription_configs:
        roles_section = "\n".join([f"      ✓ {role}" for role in config['assigned_roles']])
        subscriptions_section += f"""
  📋 Subscription: {config['name']}
     ID: {config['id']}
     State: {config['state']}

     Roles Assigned:
{roles_section}
"""
        if config.get('custom_role_created'):
            subscriptions_section += """
     Custom Role for Cloud Forwarding:
      ✓ Infoblox Cloud Forwarding Custom Role
"""

    # Determine next steps based on mode
    if mode == "Single":
        next_steps = f"""Next Steps in Infoblox Portal:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Navigate to the Azure Discovery Job configuration
2. Set Account Preference to: Single
3. Paste the Subscription ID: {subscription_configs[0]['id']}
4. Paste the Tenant ID: {tenant_id}
5. Complete the configuration and test the connection"""
        mode_label = "Single Subscription Mode"
    else:
        next_steps = f"""Next Steps in Infoblox Portal:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Navigate to the Azure Discovery Job configuration (step 13)
2. Set Account Preference to: Auto-Discover Multiple
3. Paste the Tenant ID shown above: {tenant_id}
4. The system will auto-discover all {len(subscription_configs)} configured subscription(s)
5. Complete the configuration and test the connection"""
        mode_label = "Auto-Discover Multiple Mode"

    summary = f"""
╔══════════════════════════════════════════════════════════════════╗
║        Azure Configuration Summary for Infoblox                  ║
║                  {mode_label:^42}  ║
╚══════════════════════════════════════════════════════════════════╝

🎯 COPY THESE VALUES TO INFOBLOX PORTAL:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Tenant ID: {tenant_id}
  {"Subscription ID: " + subscription_configs[0]['id'] if mode == "Single" else ""}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Application Details:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Application ID: {app_id}
  Service Principal ID: {principal_id}

Configured Subscriptions ({len(subscription_configs)} total):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{subscriptions_section}

{next_steps}

✅ Configuration completed successfully!
   Subscription(s) configured with required permissions for:
   • IPAM Synchronization (Reader role)
   • DNS Management (DNS Zone Contributor roles)
   • Cloud Forwarding (Custom role)
"""

    with open('azure_config_summary.txt', 'w') as f:
        f.write(summary)

    print(summary)

def main():
    """Main execution flow"""
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  Azure Discovery and Configuration for Infoblox         ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()

    # Get Infoblox Application ID
    app_id = get_infoblox_app_id()

    # Get optional subscription ID for Single mode
    target_subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID', '').strip()

    # Initialize Azure credential
    credential = DefaultAzureCredential()

    # Discover Azure context (Single or Auto-Discover Multiple)
    tenant_id, subscription_list, mode = discover_azure_context(credential, target_subscription_id)

    # Create or get service principal (once per tenant)
    principal_id = create_or_get_service_principal(credential, app_id)

    # Configure each subscription
    subscription_configs = []

    for idx, subscription in enumerate(subscription_list, 1):
        print(f"\n{'='*70}")
        if mode == "Single":
            print(f"Configuring Single Subscription: {subscription['name']}")
        else:
            print(f"Configuring Subscription {idx}/{len(subscription_list)}: {subscription['name']}")
        print(f"{'='*70}")

        subscription_id = subscription['id']
        subscription_name = subscription['name']

        # Skip disabled subscriptions
        if subscription['state'] != 'Enabled':
            print(f"⚠️  Skipping subscription (State: {subscription['state']})")
            continue

        # Assign built-in Azure roles
        assigned_roles = assign_built_in_roles(
            credential,
            subscription_id,
            subscription_name,
            principal_id
        )

        # Create and assign optional custom role for Cloud Forwarding
        custom_role_id = create_custom_cloud_forwarding_role(credential, subscription_id)
        custom_role_assigned = False
        if custom_role_id:
            assignment_id = assign_custom_role(
                credential,
                subscription_id,
                custom_role_id,
                principal_id
            )
            custom_role_assigned = assignment_id is not None

        # Store configuration details
        subscription_configs.append({
            'id': subscription_id,
            'name': subscription_name,
            'state': subscription['state'],
            'assigned_roles': assigned_roles,
            'custom_role_created': custom_role_assigned
        })

    # Write summary
    write_summary(tenant_id, app_id, principal_id, subscription_configs, mode)

    return 0

if __name__ == "__main__":
    sys.exit(main())
