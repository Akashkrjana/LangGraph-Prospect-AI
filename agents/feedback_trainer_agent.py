import os
import datetime
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials

# Re-using the ReAct agent code structure for the LLM analysis part
from .outreach_content_agent import run_outreach_content_agent 

# Load environment variables from .env file
load_dotenv()

# --- Main Agent Function with REAL Google Sheets Call ---

def run_feedback_trainer_agent(state: dict) -> dict:
    """
    Analyzes campaign performance, suggests improvements, and writes them to a Google Sheet.
    """
    print("\n---EXECUTING FEEDBACK TRAINER AGENT---")

    responses = state.get('responses', [])
    sent_statuses = state.get('sent_status', [])
    
    if not sent_statuses: # We need to know how many were sent to calculate rates
        print("- No sent emails to analyze. Ending feedback cycle.")
        return {"recommendations": []}

    # --- 1. Calculate Performance Metrics ---
    total_sent = len([s for s in sent_statuses if s.get('status') == 'sent'])
    positive_replies = len([r for r in responses if r.get('response_type') == 'Positive Reply'])
    
    stats = {
        "total_sent": total_sent,
        "positive_replies": positive_replies,
        "reply_rate": positive_replies / total_sent if total_sent > 0 else 0,
    }
    print(f"📊 Analyzing performance: {stats['positive_replies']}/{stats['total_sent']} positive replies ({stats['reply_rate']:.2%}).")

    # --- 2. Use an LLM to Generate Recommendations (Still Mocked for Simplicity) ---
    # A full implementation would use a ReAct prompt to analyze the stats dict.
    recommendations = []
    if stats['reply_rate'] > 0.1:
        recommendations.append("Reply rate is strong. The current strategy is effective. Recommend continuing.")
    else:
        recommendations.append("Reply rate is low. Suggest A/B testing a new subject line or email body to improve engagement.")

    if not recommendations:
        print("\n- No new recommendations were generated in this cycle.")
        return {"recommendations": []}

    # --- 3. Write Recommendations to Google Sheets (REAL Implementation) ---
    try:
        print("\n📝 Connecting to Google Sheets to write recommendations...")
        sheet_id = os.getenv("SHEET_ID")
        if not sheet_id or "your_google_sheet_id_here" in sheet_id:
            raise ValueError("Google Sheet ID not found or is a placeholder in .env file.")

        # Define the scope of access
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        
        # Authenticate using the service account credentials file
        creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
        client = gspread.authorize(creds)
        
        # Open the sheet and select the first worksheet
        sheet = client.open_by_key(sheet_id).sheet1
        
        # Append a new row for each recommendation
        for rec in recommendations:
            row = [
                datetime.date.today().isoformat(), # Timestamp
                rec, # Recommendation
                "Pending Approval" # Status
            ]
            sheet.append_row(row)
            print(f"   - ✅ Wrote: '{rec}'")

        print("\n✅ Feedback Trainer Agent finished. Suggestions sent for approval.")
    
    except FileNotFoundError:
        print("   - ❌ ERROR: 'credentials.json' not found. Please follow the setup instructions.")
    except Exception as e:
        print(f"   - ❌ ERROR: Could not write to Google Sheet. Reason: {e}")
        
    return {"recommendations": recommendations}