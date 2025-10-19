# agents/__init__.py

"""
This file makes the 'agents' directory a Python package.
It imports the main function from each agent module, allowing for easy access
from other parts of the application. It also creates a mapping from agent
names (as strings) to their corresponding functions for dynamic dispatch.
"""

# Import the primary function from each agent module
from .prospect_search_agent import run_prospect_search_agent
from .data_enrichment_agent import run_data_enrichment_agent
from .abstract_enrichment_agent import run_abstract_enrichment_agent
from .scoring_agent import run_scoring_agent
from .outreach_content_agent import run_outreach_content_agent
from .outreach_executor_agent import run_outreach_executor_agent
from .response_tracker_agent import run_response_tracker_agent
from .feedback_trainer_agent import run_feedback_trainer_agent

# Create a dictionary that maps the agent names from workflow.json to the functions
# This allows the langgraph_builder to dynamically select the correct agent function
# based on the workflow configuration.
agent_functions = {
    "ProspectSearchAgent": run_prospect_search_agent,
    "DataEnrichmentAgent": run_data_enrichment_agent,
    "AbstractEnrichmentAgent": run_abstract_enrichment_agent,
    "ScoringAgent": run_scoring_agent,
    "OutreachContentAgent": run_outreach_content_agent,
    "OutreachExecutorAgent": run_outreach_executor_agent,
    "ResponseTrackerAgent": run_response_tracker_agent,
    "FeedbackTrainerAgent": run_feedback_trainer_agent,
}