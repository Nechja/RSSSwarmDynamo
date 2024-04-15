from injector import inject
from ..infrastructure.mongodb_client import MongoDBClient
from ..infrastructure.docker_api import DockerAPI

class LeaderElectionService:
    @inject
    def __init__(self, db_client: MongoDBClient):
        self.db_client = db_client
        print("LeaderElectionService Started Up")

    def elect_leader(self):
        pass

class MonitoringService:
    @inject
    def __init__(self, docker_api: DockerAPI):
        self.docker_api = docker_api
        print("MonitoringService Started Up")

    def monitor_system(self):
        pass
