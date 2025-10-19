import os
import datetime
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Load environment variables from .env file
load_dotenv()

# --- Main Agent Function with REAL SendGrid Call ---

def run_outreach_executor_agent(state: dict) -> dict:
    """
    The main function for the Outreach Executor Agent.
    It sends the generated emails to the intended recipients using SendGrid.
    """
    print("\n---EXECUTING OUTREACH EXECUTOR AGENT---")
    
    messages_to_send = state.get('messages', [])
    if not messages_to_send:
        print("⚠️ No messages found to send. Skipping.")
        return {"sent_status": []}
        
    print(f"📨 Found {len(messages_to_send)} messages to send.")

    # Initialize the SendGrid client
    try:
        sendgrid_api_key = os.getenv("SENDGRID_API_KEY")
        from_email = os.getenv("SENDGRID_FROM_EMAIL")
        if not sendgrid_api_key or "your_sendgrid_api_key" in sendgrid_api_key:
            raise ValueError("SendGrid API key not found or is a placeholder.")
        if not from_email or "your.verified.email" in from_email:
            raise ValueError("SendGrid 'from' email not found or is a placeholder.")
        
        sg = SendGridAPIClient(sendgrid_api_key)
    except Exception as e:
        print(f"❌ ERROR: Could not initialize SendGrid client. Reason: {e}")
        return {"sent_status": []}

    delivery_statuses = []
    for message_data in messages_to_send:
        recipient_email = message_data.get("lead_email")
        full_email_body = message_data.get("email_body", "")
        
        # Simple parsing to separate subject from body
        subject_line = "A message from Analytos.ai"
        email_content = full_email_body
        if "\n\n" in full_email_body:
            subject_line = full_email_body.split("\n\n")[0]
            email_content = "\n\n".join(full_email_body.split("\n\n")[1:])

        message = Mail(
            from_email=from_email,
            to_emails=recipient_email,
            subject=subject_line,
            html_content=email_content.replace('\n', '<br>')) # Use HTML for line breaks
        
        try:
            print(f"\n🚀 Sending email to {recipient_email} via SendGrid...")
            response = sg.send(message)
            
            # Check for a successful status code (2xx)
            if 200 <= response.status_code < 300:
                print(f"   - ✅ SUCCESS: Email successfully sent (Status: {response.status_code}).")
                status = "sent"
            else:
                print(f"   - ❗️ FAILED: Email dispatch failed (Status: {response.status_code}). Body: {response.body}")
                status = "failed"
                
            delivery_statuses.append({
                "email": recipient_email,
                "status": status,
                "timestamp": datetime.datetime.now().isoformat()
            })
        except Exception as e:
            print(f"   - ❌ ERROR: An exception occurred while sending email to {recipient_email}. Reason: {e}")
            delivery_statuses.append({
                "email": recipient_email,
                "status": "error",
                "timestamp": datetime.datetime.now().isoformat()
            })

    print(f"\n✅ Outreach Executor Agent finished. Processed {len(delivery_statuses)} emails.")
    return {"sent_status": delivery_statuses}