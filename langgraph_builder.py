import json
from typing import TypedDict, List

from langgraph.graph import StateGraph, END

# Import our validation function and the dictionary of agent functions
from workflows.validator import validate_workflow
from agents import agent_functions

# --- 1. Define the State for the Graph ---
class AgentState(TypedDict):
    config: dict
    leads: List[dict]
    enriched_leads: List[dict]
    ranked_leads: List[dict]
    messages: List[dict]
    sent_status: List[dict]
    responses: List[dict]
    recommendations: List[dict]

# --- 2. Define a Helper Function to Create Agent Nodes ---
def create_agent_node(step_config: dict):
    agent_name = step_config["agent"]
    agent_function = agent_functions[agent_name]

    def agent_node(state: AgentState):
        print(f"\n--- Running Agent: {agent_name} ---")
        state['config'] = step_config.get('config', {})
        result = agent_function(state)
        return result

    return agent_node

# --- 3. NEW: Define the Routing Function for Conditional Logic ---
def should_continue_outreach(state: AgentState):
    """
    This function acts as a router. It checks if any leads meet the score threshold.
    Based on the result, it decides whether to continue to the outreach steps or end the workflow.
    """
    print("\n--- Checking Condition: Should Continue Outreach? ---")
    ranked_leads = state.get('ranked_leads', [])
    # We'll hardcode the threshold here for simplicity, matching the outreach agent
    score_threshold = 10 
    
    high_quality_leads = [lead for lead in ranked_leads if lead.get('score', 0) >= score_threshold]
    
    if len(high_quality_leads) > 0:
        print(f"--- DECISION: Yes, {len(high_quality_leads)} leads meet the threshold. Continuing to outreach. ---")
        return "continue_outreach"
    else:
        print("--- DECISION: No, no leads meet the threshold. Ending workflow. ---")
        return "end_workflow"

# --- 4. Main Application Logic ---
if __name__ == "__main__":
    print("🚀 Starting the LangGraph Prospect-to-Lead Workflow...")

    # Load and Validate the Workflow
    try:
        with open('workflows/workflow.json', 'r') as f:
            workflow_config = json.load(f)
        print("✅ Workflow configuration loaded.")
        is_valid, errors = validate_workflow(workflow_config)
        if not is_valid:
            print("❌ Workflow validation failed...")
            for error in errors: print(f"   - {error}")
            exit()
        print("✅ Workflow configuration validated successfully.")
    except FileNotFoundError:
        print("❌ ERROR: 'workflows/workflow.json' not found.")
        exit()
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        exit()

    # Build the Graph Dynamically
    workflow = StateGraph(AgentState)
    steps = workflow_config["steps"]

    # Add all the nodes to the graph
    for step in steps:
        node_function = create_agent_node(step)
        workflow.add_node(step["id"], node_function)
    print(f"✅ All {len(steps)} nodes have been added to the graph.")

    # --- UPDATED: Connect Edges Sequentially UNTIL the decision point ---
    workflow.set_entry_point("prospect_search")
    workflow.add_edge("prospect_search", "enrichment")
    workflow.add_edge("enrichment", "scoring")

    # --- NEW: Add the Conditional Edge ---
    # After the 'scoring' node, we use our routing function to decide where to go next.
    workflow.add_conditional_edges(
        "scoring",
        should_continue_outreach,
        {
            "continue_outreach": "outreach_content", # If the router returns "continue_outreach", go to this node
            "end_workflow": END # If the router returns "end_workflow", end the graph
        }
    )
    
    # --- Connect the rest of the outreach sequence ---
    workflow.add_edge("outreach_content", "send")
    workflow.add_edge("send", "response_tracking")
    workflow.add_edge("response_tracking", "feedback_trainer")
    workflow.add_edge("feedback_trainer", END) # The last node points to the end
    
    print("✅ Graph edges connected with conditional logic.")

    # Compile the graph
    app = workflow.compile()
    print("✅ Graph compiled successfully. Ready to execute.")
    
    # Execute the Workflow
    print("\n--- EXECUTING WORKFLOW ---")
    initial_state = {}
    for output in app.stream(initial_state):
        node_name = list(output.keys())[0]
        print(f"--- Finished Agent: {node_name} ---")
    
    print("\n🎉 Workflow execution complete!")