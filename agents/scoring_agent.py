import operator

# --- Main Scoring Logic ---

def _calculate_score(lead: dict, criteria: dict) -> int:
    """
    Calculates a score for a single lead based on original prospecting signals.
    """
    score = 0
    
    # This is the new, improved scoring logic
    # It uses the data that is available from the first agent
    if lead.get("signal") == "recent_funding":
        score += 15
        print(f"    - Scored 15 for signal 'recent_funding'")

    if lead.get("signal") == "hiring_for_sales":
        score += 10
        print(f"    - Scored 10 for signal 'hiring_for_sales'")

    # You can add other rules here as well.
    # For example, check the industry if it exists in the lead data.
    if lead.get("industry") == "SaaS":
         score += 20
         print(f"    - Scored 20 for industry 'SaaS'")

    return score

# --- Main Agent Function ---

def run_scoring_agent(state: dict) -> dict:
    """
    The main function for the Scoring Agent.
    It takes enriched leads and ranks them based on a scoring model.
    """
    print("\n---EXECUTING SCORING AGENT---")
    
    enriched_leads = state.get('enriched_leads', [])
    
    if not enriched_leads:
        print("⚠️ No enriched leads found to score. Skipping.")
        return {"ranked_leads": []}
        
    print(f"⚖️ Found {len(enriched_leads)} enriched leads to score.")
    
    scored_leads = []
    for lead in enriched_leads:
        # FIXED: Changed 'contact' to 'contact_name' to get the correct key
        contact_name = lead.get('contact_name', 'Unknown')
        print(f"\n  - Scoring lead: {contact_name}")
        
        # FIXED: The criteria dictionary is no longer needed, so we pass an empty one
        score = _calculate_score(lead, {})
        lead_with_score = lead.copy()
        lead_with_score['score'] = score
        scored_leads.append(lead_with_score)
        print(f"  - Final Score for {contact_name}: {score}")

    # Sort the leads by score in descending order
    ranked_leads = sorted(scored_leads, key=operator.itemgetter('score'), reverse=True)
    
    print("\n✅ Scoring Agent finished. Leads have been ranked.")
    print("Top 3 ranked leads:")
    for lead in ranked_leads[:3]:
        # FIXED: Changed 'contact' to 'contact_name' to display the name correctly
        print(f"  - {lead.get('contact_name')} (Score: {lead.get('score')})")

    return {"ranked_leads": ranked_leads}