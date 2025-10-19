import os
import time
import random
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Mock Response Tracking Function (Replace with your actual Apollo API call) ---

def _check_apollo_for_responses(api_key: str, sent_emails: list) -> list:
    """
    Mocks a call to the Apollo API to check for email responses.
    In a real implementation, you would query Apollo's analytics or webhook endpoints.
    """
    print(f"\n📡 Mocking call to Apollo API to check for responses...")
    print(f"   - Tracking {len(sent_emails)} sent emails.")
    
    # Simulate a network delay
    time.sleep(1)

    if not api_key or "your_apollo_api_key" in api_key:
        print("   - ❗️ WARNING: Apollo API key not found. No responses can be tracked.")
        return []

    # Simulate responses for a random subset of sent emails
    detected_responses = []
    possible_responses = [
        {"type": "Positive Reply", "body": "This looks interesting, let's chat next week."},
        {"type": "Meeting Booked", "body": "Thanks! I've booked a time on your calendar."},
        {"type": "Opt-out", "body": "Please remove me from your mailing list."}
    ]

    for email_info in sent_emails:
        # Simulate a 33% chance of getting a response for any given email
        if random.random() < 0.33:
            response_data = random.choice(possible_responses)
            response = {
                "email": email_info.get("email"),
                "response_type": response_data["type"],
                "response_body": response_data["body"]
            }
            detected_responses.append(response)
            print(f"   - ✅ Success: Detected a '{response['response_type']}' from {response['email']}.")

    return detected_responses

# --- Main Agent Function ---

def run_response_tracker_agent(state: dict) -> dict:
    """
    The main function for the Response Tracker Agent.
    It monitors replies and bookings for the sent outreach emails.
    
    Args:
        state (dict): The current state of the LangGraph.
                      It's expected to contain a 'sent_status' key.

    Returns:
        dict: A dictionary containing the 'responses' from the campaign.
    """
    print("\n---EXECUTING RESPONSE TRACKER AGENT---")
    
    # 1. Get the list of sent email statuses from the previous step
    all_sent_statuses = state.get('sent_status', [])
    
    # Filter for only the emails that were successfully sent
    successfully_sent_emails = [s for s in all_sent_statuses if s.get('status') == 'sent']
    
    if not successfully_sent_emails:
        print("⚠️ No successfully sent emails to track. Skipping.")
        return {"responses": []}
        
    print(f"📈 Found {len(successfully_sent_emails)} successfully sent emails to track.")

    # 2. Load Apollo API Key
    apollo_api_key = os.getenv("APOLLO_API_KEY")
    
    # 3. Check for responses
    new_responses = _check_apollo_for_responses(apollo_api_key, successfully_sent_emails)
    
    if not new_responses:
        print("\n- No new responses detected in this cycle.")
    else:
        print(f"\n✅ Response Tracker Agent finished. Detected {len(new_responses)} new responses.")
    
    # 4. Return the detected responses to the graph's state
    return {"responses": new_responses}