from .base_agent import BaseAgent

class ReviewerAgent(BaseAgent):
    def perform_task(self, task):
        # Search for relevant documentation
        docs = self.vector_db.search(task["description"])
        
        # Get open pull requests
        open_prs = self.github_client.get_open_pull_requests()
        
        for pr in open_prs:
            # In a real implementation, you would analyze the PR and generate comments
            # based on the agent's personality and the task description.
            comment = f"Review for PR #{pr.number}:\n"
            comment += f"Task: {task['name']}\n"
            comment += "Relevant documentation:\n"
            for doc in docs:
                comment += f"- {doc}\n"
            comment += "\nPlease ensure the changes align with our coding standards and the task requirements."

            self.github_client.comment_on_pull_request(pr.number, comment)

            # Example of suggesting changes (you would generate these based on the actual PR content)
            suggestions = {
                "example_file.py": "Consider using a more descriptive variable name here."
            }
            self.github_client.suggest_changes(pr.number, suggestions)