# LangGraph-Powered Autonomous B2B Lead Generation Agent

This project is an end-to-end autonomous agent system that discovers, enriches, scores, and contacts B2B prospects. Built with LangGraph, the entire workflow is dynamically configured and executed from a single `workflow.json` file, making it highly modular and easy to modify. The system is designed to automate the outbound lead generation process for B2B companies in the USA with revenues between $20M-$200M. A key feature is the `FeedbackTrainerAgent`, which analyzes campaign results and suggests improvements over time.

## ✨ Key Features

* **AI-Assisted Development**: The project was built using an AI-assisted "vibe coding" approach to accelerate development.
* **Dynamic Configuration**: Uses a single `workflow.json` as the source of truth for dynamically constructing the agent graph.
* **Modular Sub-Agents**: Each step in the workflow is a self-contained Python script located in the `/agents/` directory, making the system easy to extend.
* **ReAct Prompting**: Employs the ReAct (Reason+Act) prompting framework for more advanced and transparent agent reasoning.
* **Conditional Logic**: The workflow supports conditional flows, allowing it to make decisions like skipping outreach for low-scoring leads.
* **Automated Feedback Loop**: Includes a `FeedbackTrainerAgent` that analyzes campaign performance, suggests configuration changes, and writes them to a Google Sheet for human approval.

## 🌊 Workflow Diagram

The application follows a conditional workflow:

`[Prospect Search]` -> `[Enrichment]` -> `[Scoring]`
* **If Score is High** -> `[Outreach Content]` -> `[Send Email]` -> `[Track Response]` -> `[Feedback Trainer]` -> `[End]`
* **If Score is Low** -> `[End]`

## 🛠️ Tech Stack

| Component         | Tool / Library          | Purpose                                        |
| :---------------- | :---------------------- | :--------------------------------------------- |
| Agent Framework   | LangGraph + LangChain   | Core orchestration of the agent workflow.      |
| LLM               | OpenAI GPT-4o-mini      | For advanced reasoning and content generation. |
| Data APIs         | Clay API, Apollo API    | Used for B2B prospect discovery.               |
| Enrichment        | Abstract API            | For enriching company and contact data.        |
| Email Delivery    | SendGrid                | For programmatically sending outreach emails.  |
| Config & Logging  | Google Sheets API       | Used by the feedback loop to log recommendations. |

## 📂 Project Structure
LangGraphProspectAI/ ├── agents/ │ ├── init.py │ ├── abstract_enrichment_agent.py │ ├── feedback_trainer_agent.py │ ├── outreach_content_agent.py │ ├── outreach_executor_agent.py │ ├── prospect_search_agent.py │ ├── response_tracker_agent.py │ └── scoring_agent.py ├── workflows/ │ ├── workflow.json │ └── validator.py ├── .env.example ├── .gitignore ├── credentials.json ├── langgraph_builder.py ├── README.md └── requirements.txt

## ⚙️ Setup and Installation

Follow these steps to get the project running on your local machine.

### 1. Prerequisites
* Python 3.9+
* Git

### 2. Clone the Repository
```bash
git clone [https://github.com/YourUsername/LangGraph-Prospect-AI.git](https://github.com/YourUsername/LangGraph-Prospect-AI.git)
cd LangGraph-Prospect-AI

3. Set Up the Environment
Create and activate a Python virtual environment.

# Create the environment
python -m venv venv

# Activate on Windows
.\venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate

4. Install Dependencies
Install all the required Python libraries.

pip install -r requirements.txt

5. Configure API Keys (.env)
Make a copy of the example environment file: copy .env.example .env (on Windows) or cp .env.example .env (on Mac/Linux).

Open the new .env file and replace the placeholder values with your actual secret keys from OpenAI, SendGrid, Abstract API, etc.

6. Configure Google Sheets (credentials.json)
Follow the Google Cloud documentation to create a Service Account.

Enable the Google Sheets API and Google Drive API.

Download the JSON key for your service account and save it as credentials.json in the project root.

Open credentials.json, copy the client_email, and share your Google Sheet with that email, giving it Editor permissions.

🚀 How to Run the Application
Once your setup is complete, you can run the entire workflow.

(Optional) Validate the Workflow:

python workflows/validator.py

Run the Main Application:

python langgraph_builder.py

🔧 How to Customize and Extend
The primary control panel is the workflows/workflow.json file. To change the target market, simply edit the config block for the prospect_search step. To add a new agent, create its file, register it in agents/__init__.py, and add a new step for it in workflow.json.

---
## How to Paste Correctly

1.  **Click the "Copy" button** on the code block above.
2.  Go to your **`README.md`** file in VS Code.
3.  **Delete everything** currently in the file.
4.  **Paste** the new, clean content.
5.  Open the **Markdown Preview** (`Ctrl+Shift+V`) to confirm that it now has the proper headings, tables, and lists.