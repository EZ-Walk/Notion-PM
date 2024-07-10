import os
import time
from dotenv import load_dotenv
from notion_client import NotionClient
from github_client import GitHubClient
from vector_db import VectorDB
from agents.coder_agent import CoderAgent
from agents.reviewer_agent import ReviewerAgent

load_dotenv()

def main():
    notion_client = NotionClient(
        os.getenv("NOTION_API_KEY"),
        os.getenv("NOTION_AGENTS_DB_ID"),
        os.getenv("NOTION_TASKS_DB_ID")
    )
    github_client = GitHubClient(
        os.getenv("GITHUB_API_TOKEN"),
        os.getenv("GITHUB_REPO_OWNER"),
        os.getenv("GITHUB_REPO_NAME")
    )
    vector_db = VectorDB()

    while True:
        try:
            agents = notion_client.get_agents()
            tasks = notion_client.get_tasks()

            for task in tasks:
                assigned_agent = next((agent for agent in agents if agent["id"] == task["assignee"]), None)
                if assigned_agent:
                    if assigned_agent["role"] == "coder":
                        agent = CoderAgent(github_client, vector_db)
                    elif assigned_agent["role"] == "reviewer":
                        agent = ReviewerAgent(github_client, vector_db)
                    else:
                        print(f"Unknown agent role: {assigned_agent['role']}")
                        continue

                    agent.perform_task(task)
                    notion_client.mark_task_complete(task["id"])

            time.sleep(60)  # Wait for 1 minute before checking for new tasks
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            time.sleep(60)  # Wait for 1 minute before retrying

if __name__ == "__main__":
    main()