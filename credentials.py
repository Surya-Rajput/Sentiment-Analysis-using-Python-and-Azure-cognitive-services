from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

API_KEY = 'PUT YOUR API KEY'
ENDPOINT = 'PUT YOUR ENDPOINT'

def client():
    try:
        client = TextAnalyticsClient(
            endpoint = ENDPOINT,
            credential = AzureKeyCredential(API_KEY)
        )
        return client
    except Exception as e:
        print(e)
        return 
