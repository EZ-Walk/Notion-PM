from .base_agent import BaseAgent

class CoderAgent(BaseAgent):
    def perform_task(self, task):
        # Search for relevant documentation
        docs = self.vector_db.search(task["description"])
        
        # In a real implementation, you would use the agent's personality and the task description
        # to generate code or modifications. For now, we'll just create a simple file.
        file_content = f"// Task: {task['name']}\n// Documentation references:\n"
        for doc in docs:
            file_content += f"// - {doc}\n"
        file_content += f"\n// TODO: Implement {task['name']}\n"

        self.github_client.create_or_update_file(
            f"{task['name'].lower().replace(' ', '_')}.txt",
            file_content,
            f"Implement {task['name']}"
        )