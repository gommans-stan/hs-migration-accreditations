import os
import requests

def main(event):
    # Accessing the API token set in HubSpot's environment variables
    hubspot_api_token = os.getenv('hubspot_apiToken')
    
    # Accessing matchRecordId from the event object provided by the workflow
    match_record_id = event['inputFields']['matchRecordId']

    headers = {
        "Authorization": f"Bearer {hubspot_api_token}",
        "Content-Type": "application/json"
    }

    def fetch_associated_vacature_ids(match_record_id):
        url = f"https://api.hubapi.com/crm/v4/objects/kandidaten/{match_record_id}/associations/vacatures"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            vacature_ids = [assoc['toObjectId'] for assoc in data.get('results', [])]
            return vacature_ids
        else:
            print(f"Failed to fetch associated Vacature IDs for Match Record ID {match_record_id}: {response.text}")
            return []

    def fetch_associated_company_id(vacature_id):
        url = f"https://api.hubapi.com/crm/v4/objects/vacatures/{vacature_id}/associations/companies"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get('results'):
                company_ids = [assoc['toObjectId'] for assoc in data.get('results', []) if 'toObjectId' in assoc]
                if company_ids:
                    return company_ids[0]
        print(f"Failed to fetch associated Company ID for Vacature ID {vacature_id}: {response.text}")
        return None

    def associate_company_with_match(match_record_id, company_id):
        url = f"https://api.hubapi.com/crm/v4/objects/kandidaten/{match_record_id}/associations/default/companies/{company_id}"
        response = requests.put(url, headers=headers)
        if response.status_code in [200, 201]:
            print(f"Successfully associated Company ID {company_id} with Match Record ID: {match_record_id}")
        else:
            print(f"Failed to associate Company ID {company_id} with Match Record ID {match_record_id}: {response.text}")

    vacature_ids = fetch_associated_vacature_ids(match_record_id)
    for vacature_id in vacature_ids:
        company_id = fetch_associated_company_id(vacature_id)
        if company_id:
            associate_company_with_match(match_record_id, company_id)
        else:
            print(f"No Company ID found for Vacature ID: {vacature_id}")