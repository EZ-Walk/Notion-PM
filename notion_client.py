from notion_client import Client

class NotionClient:
    def __init__(self, api_key, agents_db_id, tasks_db_id):
        self.client = Client(auth=api_key)
        self.agents_db_id = agents_db_id
        self.tasks_db_id = tasks_db_id

    def get_agents(self):
        response = self.client.databases.query(database_id=self.agents_db_id)
        agents = []
        for result in response["results"]:
            agents.append({
                "id": result["id"],
                "name": result["properties"]["Name"]["title"][0]["text"]["content"],
                "personality": result["properties"]["Personality"]["rich_text"][0]["text"]["content"],
                "role": result["properties"]["Role"]["select"]["name"]
            })
        return agents

    def get_tasks(self):
        response = self.client.databases.query(database_id=self.tasks_db_id)
        tasks = []
        for result in response["results"]:
            tasks.append({
                "id": result["id"],
                "name": result["properties"]["Name"]["title"][0]["text"]["content"],
                "assignee": result["properties"]["Assignee"]["relation"][0]["id"],
                "description": result["properties"]["Description"]["rich_text"][0]["text"]["content"]
            })
        return tasks

    def mark_task_complete(self, task_id):
        self.client.pages.update(
            page_id=task_id,
            properties={"Status": {"select": {"name": "Completed"}}}
        )