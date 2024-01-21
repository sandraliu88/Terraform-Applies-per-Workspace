import requests
from datetime import datetime, timedelta

def get_total_applies_per_workspace(api_token, organization_name, start_date, end_date):
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/vnd.api+json',
    }

    # Get organization ID
    org_response = requests.get(f'https://app.terraform.io/api/v2/organizations/{organization_name}', headers=headers)
    org_id = org_response.json()['data']['id']

    total_applies_by_workspace = {}

    workspaces_url = f'https://app.terraform.io/api/v2/organizations/{org_id}/workspaces'

    # Loop through all workspace pages
    while workspaces_url:
        workspaces_response = requests.get(workspaces_url, headers=headers)
        workspaces_data = workspaces_response.json().get('data', [])

        # Loop through workspaces in the current page
        for workspace in workspaces_data:
            workspace_id = workspace['id']

            # Get runs for the workspace
            runs_url = f'https://app.terraform.io/api/v2/workspaces/{workspace_id}/runs'
            runs_response = requests.get(
                runs_url,
                headers=headers,
                params={'filter[status]': 'applied', 'filter[applied-at]': f'{start_date.isoformat()},{(end_date + timedelta(days=1)).isoformat()}'}
            )

            # Check if 'data' is present in the response
            runs_data = runs_response.json().get('data', [])
            
            # Count the applies for the workspace
            total_applies_count = len(runs_data)
            workspace_name = workspace['attributes']['name']

            # Update the total applies for the workspace
            total_applies_by_workspace[workspace_name] = total_applies_by_workspace.get(workspace_name, 0) + total_applies_count

            print(f"Workspace '{workspace_name}': {total_applies_count} applies for {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")

        # Get the next page of workspaces, if available
        workspaces_url = workspaces_response.json().get('links', {}).get('next', None)

    return total_applies_by_workspace

if __name__ == "__main__":
    # Replace with your Terraform Cloud API token and organization name
    api_token = "UcyouqwOwc3jSQ.atlasv1.teR7F1rL81ydw6BOtCwdjBeDHcT03jo5jF779V8NeXKwjq6FNZYxcqz5GeWE81cqyzw"
    organization = "sandraliu-training"
    start_date = datetime(2023, 12, 1)
    end_date = datetime(2023, 12, 31)

    total_applies_by_workspace = get_total_applies_per_workspace(api_token, organization, start_date, end_date)

    for workspace, total_applies in total_applies_by_workspace.items():
        print(f"Total Applies in {workspace}: {total_applies} for {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
