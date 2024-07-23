from notion_client import Client

class NotionClient(Client):
    def __init__(self, api_key):
        super().__init__(auth=api_key)
        """
        Initializes the NotionClient with the provided API key, agents database ID, and tasks database ID.
        
        Parameters:
            api_key (str): The API key used for authentication.
            agents_db_id (str): The ID of the agents database.
            tasks_db_id (str): The ID of the tasks database.
        """
        # self.client = Client(auth=api_key)
        # self.agents_db_id = agents_db_id
        # self.tasks_db_id = tasks_db_id

    def get_agents(self):
        """
        Retrieves the list of agents by querying the agents database using the provided agents database ID.
        
        Returns:
            list: A list of dictionaries, where each dictionary represents an agent with keys 'id', 'name', 'personality', and 'role'.
        """
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
        """
        Retrieves the list of tasks by querying the tasks database using the provided tasks database ID.
        
        Returns:
            list: A list of dictionaries, where each dictionary represents a task with keys 'id', 'name', 'assignee', and 'description'.
        """
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
        """
        Marks a task as complete by updating its status in the Notion database.

        Parameters:
            task_id (str): The ID of the task to mark as complete.

        Returns:
            None
        """
        self.client.pages.update(
            page_id=task_id,
            properties={"Status": {"select": {"name": "Completed"}}}
        )