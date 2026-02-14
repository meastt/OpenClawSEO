import os
import json
from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build

def get_gsc_data():
    # Load credentials from the secret environment variable
    service_account_info = json.loads(os.environ.get('GSC_JSON_KEY'))
    # Fix double-escaped newlines in private key from .env storage
    if 'private_key' in service_account_info:
        service_account_info['private_key'] = service_account_info['private_key'].replace('\\n', '\n')
    scopes = ['https://www.googleapis.com/auth/webmasters.readonly']
    credentials = service_account.Credentials.from_service_account_info(
        service_account_info, scopes=scopes
    )

    service = build('searchconsole', 'v1', credentials=credentials)
    site_url = os.environ.get('GSC_SITE_URL', os.environ.get('WP_URL', '').rstrip('/') + '/')

    # Dynamic date range: last 28 days
    end_date = datetime.now().date() - timedelta(days=3)  # GSC data has ~3 day lag
    start_date = end_date - timedelta(days=28)

    # Query: Top 10 declining keywords
    request = {
        'startDate': str(start_date),
        'endDate': str(end_date),
        'dimensions': ['query'],
        'rowLimit': 10
    }

    return service.searchanalytics().query(siteUrl=site_url, body=request).execute()

if __name__ == "__main__":
    print(json.dumps(get_gsc_data()))