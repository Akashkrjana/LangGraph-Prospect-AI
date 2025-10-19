import json
import os
from typing import Tuple
from jsonschema import validate, ValidationError

# To make this script work, we need to know the path to the main project root
# This allows us to import from the 'agents' package correctly
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from agents import agent_functions

# Define the required structure of the workflow.json file
WORKFLOW_SCHEMA = {
    "type": "object",
    "properties": {
        "workflow_name": {"type": "string"},
        "description": {"type": "string"},
        "steps": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "agent": {"type": "string"},
                    "config": {"type": "object"},
                    "tools": {"type": "array", "items": {"type": "string"}},
                    "output_key": {"type": "string"}
                },
                "required": ["id", "agent", "config"]
            }
        }
    },
    "required": ["workflow_name", "steps"]
}

def validate_workflow(config: dict) -> Tuple[bool, list]:
    """
    Validates a workflow configuration dictionary against a schema and logical rules.

    Args:
        config (dict): The loaded workflow JSON data.

    Returns:
        tuple: A boolean indicating validity (True/False) and a list of error strings.
    """
    errors = []

    # 1. Validate against the basic JSON schema
    try:
        validate(instance=config, schema=WORKFLOW_SCHEMA)
    except ValidationError as e:
        errors.append(f"Schema Error: {e.message} in {list(e.path)}")
        return False, errors

    # 2. Perform logical validation if schema is OK
    step_ids = set()
    valid_agent_names = agent_functions.keys()

    for i, step in enumerate(config.get('steps', [])):
        step_id = step.get('id')
        agent_name = step.get('agent')

        # Check for unique step IDs
        if step_id in step_ids:
            errors.append(f"Logical Error: Duplicate step 'id' found: '{step_id}'")
        step_ids.add(step_id)

        # Check if the agent name is valid and exists in our code
        if agent_name not in valid_agent_names:
            errors.append(f"Logical Error in step '{step_id}': Agent '{agent_name}' is not a valid agent. Available agents: {list(valid_agent_names)}")

    is_valid = len(errors) == 0
    return is_valid, errors

# This allows the script to be run directly from the command line
if __name__ == "__main__":
    print("--- Running Workflow Validator ---")
    
    # Construct the path to workflow.json relative to this script's location
    workflow_file_path = os.path.join(os.path.dirname(__file__), 'workflow.json')

    try:
        with open(workflow_file_path, 'r') as f:
            workflow_config = json.load(f)
        print("✅ Successfully loaded 'workflow.json'.")

        is_valid, error_list = validate_workflow(workflow_config)

        if is_valid:
            print("\n🎉 Validation successful! The workflow.json file is well-formed and logically correct.")
        else:
            print(f"\n❌ Validation failed with {len(error_list)} errors:")
            for error in error_list:
                print(f"   - {error}")

    except FileNotFoundError:
        print(f"❌ ERROR: 'workflow.json' not found at path: {workflow_file_path}")
    except json.JSONDecodeError as e:
        print(f"❌ ERROR: Invalid JSON in 'workflow.json'. Details: {e}")