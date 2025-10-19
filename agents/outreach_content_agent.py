import os
import re
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

def run_outreach_content_agent(state: dict) -> dict:
    """
    Generates personalized emails for high-scoring leads using a ReAct prompting strategy.
    """
    print("\n---EXECUTING OUTREACH CONTENT AGENT (ReAct)---")
    
    ranked_leads = state.get('ranked_leads', [])
    if not ranked_leads:
        print("⚠️ No ranked leads to generate content for. Skipping.")
        return {"messages": []}

    agent_config = state.get('config', {})
    score_threshold = agent_config.get('score_threshold', 10)
    top_leads = [lead for lead in ranked_leads if lead.get('score', 0) >= score_threshold]
    
    if not top_leads:
        print(f"⚠️ No leads met the score threshold of {score_threshold}. Skipping outreach.")
        return {"messages": []}
        
    print(f"✍️ Found {len(top_leads)} leads to generate content for using ReAct prompting.")

    try:
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key or "your_openai_api_key_here" in openai_api_key:
            raise ValueError("OpenAI API key not found or is a placeholder.")
        client = OpenAI(api_key=openai_api_key)
    except Exception as e:
        print(f"❌ ERROR: Could not initialize OpenAI client. Reason: {e}")
        return {"messages": []}

    persona = agent_config.get('persona', 'SDR at Analytos.ai')
    tone = agent_config.get('tone', 'friendly yet professional')

    outreach_messages = []
    for lead in top_leads:
        try:
            contact_name = lead.get('contact_name', 'there')
            company_name = lead.get('company', 'your company')
            
            print(f"\n🤖 Generating email for {contact_name} at {company_name}...")
            
            react_prompt = f"""
            You are a world-class {persona}. Your tone should be {tone}.
            Your task is to write a personalized outreach email to a prospect.
            
            First, you must reason about the prospect and plan your email. This is your "Thought" process.
            Second, you must write the email itself. This is your "Action".

            You MUST respond in the following format:

            Thought:
            [Here, you will analyze the prospect's data and outline the angle you will take in the email. Mention the key personalization point you will use.]

            Email:
            [Here, you will write the final email body. It must start with "Hi {contact_name}," and should not include a subject line.]

            ---
            Prospect Data:
            - Contact Name: {contact_name}
            - Company: {company_name}
            - Signal: {lead.get('signal', 'N/A')}
            - Score: {lead.get('score', 0)}
            ---
            """
            
            completion = client.chat.completions.create(
              model="gpt-4o-mini",
              messages=[{"role": "user", "content": react_prompt}],
              temperature=0.7,
            )
            
            llm_response = completion.choices[0].message.content

            thought_match = re.search(r"Thought:(.*?)Email:", llm_response, re.DOTALL)
            email_match = re.search(r"Email:(.*)", llm_response, re.DOTALL) # <-- FIX IS HERE

            if not email_match:
                raise ValueError("LLM did not follow the ReAct format. Could not find 'Email:' section.")

            thought_process = thought_match.group(1).strip() if thought_match else "No thought process found."
            email_body = email_match.group(1).strip()

            print(f"   - 🤔 LLM Thought Process: {thought_process}")
            print(f"   - ✅ Success: Generated personalized email for {contact_name}.")
            
            message_data = {
                "lead_email": lead.get('email'),
                "email_body": f"Subject: Idea for {company_name}\n\n{email_body}"
            }
            outreach_messages.append(message_data)

        except Exception as e:
            print(f"   - ❗️ ERROR: Could not generate email for {contact_name}. Reason: {e}")
        
    print(f"\n✅ Outreach Content Agent finished. Generated {len(outreach_messages)} messages using ReAct.")
    return {"messages": outreach_messages}