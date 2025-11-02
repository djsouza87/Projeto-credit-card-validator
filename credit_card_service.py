import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from utils.Config import Config

def analyze_credit_card(card_url, debug: bool = False):
    
    credential = AzureKeyCredential(Config.KEY)
    document_client = DocumentIntelligenceClient(Config.ENDPOINT, credential)

    card_info = document_client.begin_analyze_document(
        "prebuilt-creditCard", AnalyzeDocumentRequest(url_source=card_url)
    )
    result = card_info.result()
        
    for document in result.documents:
        fields = document.get("Fields", {})

        return {
            "card_name": fields.get("CardholderName", {}).get('content'),
            "card_number": fields.get("CardNumber", {}).get('content'),
            "bank_name": fields.get("Issuer", {}).get('content'),
            "expiry_date": fields.get("ExpirationDate", {}).get('content'),
        }
    