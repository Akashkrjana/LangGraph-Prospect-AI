import os
import time
import random
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Mock API Function (Replace with your actual API calls) ---

def _call_clearbit_api(api_key: str, lead: dict):
    """
    Mocks a call to the Clearbit Enrichment API for a given lead.
    In a real implementation, you would use the lead's email or company domain
    to fetch data from Clearbit.
    """
    email = lead.get("email", "N/A")
    print(f"\n💧 Mocking call to Clearbit API for: {email}")
    
    # Simulate a network delay
    time.sleep(1)
    
    if not api_key or api_key == "your_clearbit_key":
        print(f"   - WARNING: Clearbit API key not found. Skipping enrichment for {email}.")
        # Return the original lead data with an empty technologies field
        return {
            "company": lead.get("company"),
            "contact": lead.get("contact_name"),
            "role": "Unknown",
            "technologies": []
        }
    
    # Simulate finding different roles and tech stacks for variety
    mock_roles = ["VP of Sales", "Marketing Director", "Product Manager", "Sales Manager"]
    mock_tech_stacks = [
        ["Salesforce", "HubSpot", "AWS", "Zoom"],
        ["Marketo", "GCP", "Outreach.io"],
        ["Salesforce", "Slack", "Jira"],
    ]
    
    enriched_data = {
        "company": lead.get("company"),
        "contact": lead.get("contact_name"),
        "role": random.choice(mock_roles),
        "technologies": random.choice(mock_tech_stacks)
    }
    
    print(f"   - Success: Enriched {email} with role '{enriched_data['role']}'.")
    return enriched_data

# --- Main Agent Function ---

def run_data_enrichment_agent(state: dict) -> dict:
    """
    The main function for the Data Enrichment Agent.
    It takes a list of leads and enriches them with additional data.
    
    Args:
        state (dict): The current state of the LangGraph. 
                      It's expected to contain a 'leads' key.

    Returns:
        dict: A dictionary with the new 'enriched_leads' data.
    """
    print("\n---EXECUTING DATA ENRICHMENT AGENT---")
    
    # 1. Get the list of leads from the previous step
    leads_to_enrich = state.get('leads', [])
    
    if not leads_to_enrich:
        print("⚠️ No leads found to enrich. Skipping.")
        return {"enriched_leads": []}
        
    print(f"📂 Found {len(leads_to_enrich)} leads to enrich.")
    
    # 2. Load the API key from environment variables
    clearbit_api_key = os.getenv("CLEARBIT_KEY")
    
    # 3. Loop through each lead and enrich it
    enriched_leads = []
    for lead in leads_to_enrich:
        enriched_data = _call_clearbit_api(clearbit_api_key, lead)
        enriched_leads.append(enriched_data)
        
    print(f"\n✅ Data Enrichment Agent finished. Total leads enriched: {len(enriched_leads)}")
    
    # 4. Return the results to be added to the graph's state
    return {"enriched_leads": enriched_leads}