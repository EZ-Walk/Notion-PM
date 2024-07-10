from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(self, github_client, vector_db):
        self.github_client = github_client
        self.vector_db = vector_db

    @abstractmethod
    def perform_task(self, task):
        pass