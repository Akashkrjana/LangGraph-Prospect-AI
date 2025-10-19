import os
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Mock API Functions (Replace with your actual API calls) ---

def _call_apollo_api(api_key: str, icp: dict):
    """
    Mocks a call to the Apollo.io API to find leads.
    In a real implementation, you would use a library like 'requests'
    to make an HTTP POST request to Apollo's search endpoint.
    """
    print(f"\n📞 Mocking call to Apollo API...")
    print(f"   - Searching with ICP: {icp}")
    
    # Simulate a network delay
    time.sleep(1) 
    
    if not api_key or api_key == "your_apollo_api_key":
        print("   - WARNING: Apollo API key not found. Returning empty list.")
        return []
    
    # Return fake data that matches the expected output schema
    mock_leads = [
        {
            "company": "Innovate Inc.", 
            "contact_name": "Alex Johnson", 
            "email": "alex.j@innovate.com", 
            "linkedin": "linkedin.com/in/alexjohnsoninnovate", 
            "signal": "hiring_for_sales"
        },
        {
            "company": "Tech Solutions LLC", 
            "contact_name": "Maria Garcia", 
            "email": "maria.g@techsolutions.com", 
            "linkedin": "linkedin.com/in/mariagarciatech", 
            "signal": "recent_funding"
        }
    ]
    print(f"   - Success: Found {len(mock_leads)} leads from Apollo.")
    return mock_leads

def _call_clay_api(api_key: str, icp: dict):
    """
    Mocks a call to the Clay.com API to find and enrich leads.
    """
    print(f"\n🧱 Mocking call to Clay API...")
    print(f"   - Searching with ICP: {icp}")
    
    time.sleep(1)
    
    if not api_key or api_key == "your_clay_api_key":
        print("   - WARNING: Clay API key not found. Returning empty list.")
        return []
    
    mock_leads = [
        {
            "company": "DataDriven Co.", 
            "contact_name": "Sam Chen", 
            "email": "sam.c@datadriven.com", 
            "linkedin": "linkedin.com/in/samchendata", 
            "signal": "hiring_for_sales"
        }
    ]
    print(f"   - Success: Found {len(mock_leads)} leads from Clay.")
    return mock_leads

# --- Main Agent Function ---

def run_prospect_search_agent(state: dict) -> dict:
    """
    The main function for the Prospect Search Agent.
    It orchestrates fetching leads from various data sources based on the ICP.
    
    Args:
        state (dict): The current state of the LangGraph, containing agent configuration.

    Returns:
        dict: A dictionary with the new data to be merged into the state.
    """
    print("\n---EXECUTING PROSPECT SEARCH AGENT---")
    
    # 1. Load API keys from environment variables
    apollo_api_key = os.getenv("APOLLO_API_KEY")
    clay_api_key = os.getenv("CLAY_API_KEY")

    # 2. Get the Ideal Customer Profile (ICP) from the state
    # We assume the builder script places the step's config into the state.
    agent_config = state.get('config', {})
    icp = {
        "industry": agent_config.get("industry"),
        "location": agent_config.get("location"),
        "employee_count": agent_config.get("employee_count"),
        "revenue": agent_config.get("revenue"),
        "signals": agent_config.get("signals")
    }
    print(f"🔍 Starting prospect search with ICP: {icp}")

    # 3. Call the data source APIs
    apollo_leads = _call_apollo_api(apollo_api_key, icp)
    clay_leads = _call_clay_api(clay_api_key, icp)
    
    # 4. Combine and de-duplicate leads
    # (In a real scenario, you'd have logic to merge and avoid duplicates)
    all_leads = apollo_leads + clay_leads
    
    print(f"\n✅ Prospect Search Agent finished. Total leads found: {len(all_leads)}")
    
    # 5. Return the results to be added to the graph's state
    # The key 'leads' will hold the output of this agent.
    return {"leads": all_leads}