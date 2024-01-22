import requests
from datetime import datetime, timedelta

def get_applies_by_workspace(api_token, organization_name, start_date, end_date):
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/vnd.api+json'
    }

    # Get organization information
    org_url = f'https://app.terraform.io/api/v2/organizations/{organization_name}'
    org_response = requests.get(org_url, headers=headers)
    org_data = org_response.json()
    org_id = org_data['data']['id']

    # Get workspaces in the organization
    workspaces_url = f'https://app.terraform.io/api/v2/organizations/{org_id}/workspaces'
    applies_by_workspace = {}

    while workspaces_url:
        workspaces_response = requests.get(workspaces_url, headers=headers)
        workspaces_data = workspaces_response.json()

        for workspace in workspaces_data.get('data', []):
            workspace_id = workspace['id']
            workspace_name = workspace['attributes']['name']
            
            # Get the runs (applies) for the workspace within the specified timeframe
            runs_url = f'https://app.terraform.io/api/v2/workspaces/{workspace_id}/runs'
            runs_response = requests.get(runs_url, headers=headers)
            runs_data = runs_response.json()

            applies_count = 0
            for run in runs_data.get('data', []):
                run_timestamp = datetime.strptime(run['attributes']['created-at'], '%Y-%m-%dT%H:%M:%S.%fZ')
                
                if start_date <= run_timestamp <= end_date and run['attributes']['status'] == 'applied':
                    applies_count += 1

            applies_by_workspace[workspace_name] = applies_count

        # Check if there are more pages of workspaces
        workspaces_url = workspaces_data['links'].get('next', None)

    return applies_by_workspace

# Replace 'YOUR_API_TOKEN' and 'YOUR_ORG_NAME' with your actual API token and organization name
api_token = 'YOUR_API_TOKEN'
organization_name = 'YOUR_ORG_NAME'

# Specify the start and end dates for the monthly timeframe
start_date = datetime(2023, 5, 1)  # Replace with your desired start date
end_date = datetime(2023, 5, 31)   # Replace with your desired end date

applies_by_workspace = get_applies_by_workspace(api_token, organization_name, start_date, end_date)

# Display applies by workspace
for workspace, applies_count in applies_by_workspace.items():
    print(f'Workspace: {workspace}, Applies: {applies_count}')