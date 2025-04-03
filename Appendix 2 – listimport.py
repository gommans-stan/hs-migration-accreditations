import pandas as pd
import requests
import os
import time

# Ensure you replace `your_portal_id` and `your_hubspot_api_key` with actual values.
# This script directly uses contact IDs from Excel files to add them to HubSpot lists.
# Configuration
api_key = 'REDACTED'
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}
folder_path = '../'


def create_hubspot_list(name):
    payload = {
        "name": name,
        "dynamic": False,
        "portalId": 139689567, 
        "filters": []
    }
    response = requests.post('https://api.hubapi.com/contacts/v1/lists', headers=headers, json=payload)
    if response.status_code in [200, 201]:  # Accept both 200 and 201 as successful
        return response.json()['listId']
    else:
        print(f"API Response for creating list '{name}': {response.status_code} - {response.text}")
        return None

def add_contacts_to_list(list_id, contact_ids):
    payload = {"vids": contact_ids}
    response = requests.post(f'https://api.hubapi.com/contacts/v1/lists/{list_id}/add', headers=headers, json=payload)
    if response.status_code in [200, 202]:
        print(f"Successfully added contacts to list ID {list_id}.")
    else:
        print(f"Failed to add contacts to list {list_id}. API Response: {response.status_code} - {response.text}")


# Main loop to process Excel files
for filename in os.listdir(folder_path):
    if filename.endswith('.xlsx'):
        file_path = os.path.join(folder_path, filename)
        df = pd.read_excel(file_path, engine='openpyxl')
        
        contact_ids = df.iloc[:, 0].tolist()  # Include all contact IDs

        if contact_ids:
            # Create a HubSpot list
            list_name = filename.replace('.xlsx', '')
            list_id = create_hubspot_list(list_name)
            if list_id:
                # Add contacts to the list
                add_contacts_to_list(list_id, contact_ids)
            else:
                print(f"Failed to create list for {list_name}")
        else:
            print(f"No contact IDs found in {filename}")
