# agents/abstract_enrichment_agent.py
import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

def _get_domain_from_company_name(company_name: str) -> str:
    """A simple helper to guess a domain from a company name."""
    # Example: "Innovate Inc." -> "innovateinc.com"
    return company_name.lower().replace(' ', '').replace('.', '').replace(',', '').replace('inc', '').replace('llc', '') + ".com"

def run_abstract_enrichment_agent(state: dict) -> dict:
    """
    Enriches lead data using the Abstract Company Enrichment API.
    """
    print("\n---EXECUTING ABSTRACT API ENRICHMENT AGENT---")
    
    leads_to_enrich = state.get('leads', [])
    if not leads_to_enrich:
        print("⚠️ No leads found to enrich. Skipping.")
        return {"enriched_leads": []}
        
    print(f"📂 Found {len(leads_to_enrich)} leads to enrich using Abstract API.")
    
    api_key = os.getenv("ABSTRACT_API_KEY")
    if not api_key or "your_new_abstract_api_key_here" in api_key:
        print("❌ ERROR: Abstract API key not found or is a placeholder in .env file.")
        return {"enriched_leads": []}

    enriched_leads = []
    for lead in leads_to_enrich:
        try:
            company_name = lead.get("company")
            # Abstract API needs a domain, so we'll guess it from the company name.
            domain = _get_domain_from_company_name(company_name)
            
            print(f"\n💧 Enriching company: {company_name} (domain: {domain})")

            # Make the actual API call to Abstract API
            response = requests.get(
                f"https://companyenrichment.abstractapi.com/v1/?api_key={api_key}&domain={domain}"
            )
            response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
            
            data = response.json()
            
            # Map the response data to our desired structure
            # Start with a copy of the original lead to preserve all its data
            enriched_data = lead.copy()

            # Now, add or update it with the new data from Abstract API
            enriched_data.update({
                "company": data.get("name", company_name), # Updates the company name if a better one is found
                "role": "Unknown", # Still unknown
                "technologies": [] # Still unknown
            })
            enriched_leads.append(enriched_data)
            print(f"   - Success: Enriched {company_name}.")
            
            # Abstract API's free plan has a rate limit of 1 request per second
            time.sleep(1)

        except requests.exceptions.RequestException as e:
            print(f"   - ❗️ ERROR: Could not enrich {company_name}. Reason: {e}")
        except Exception as e:
            print(f"   - ❗️ An unexpected error occurred for {company_name}: {e}")
            
    print(f"\n✅ Abstract API Enrichment Agent finished. Total leads enriched: {len(enriched_leads)}")
    return {"enriched_leads": enriched_leads}