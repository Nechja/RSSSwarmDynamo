from ..infrastructure.mongodb_client import MongoDBClient
from ..infrastructure.docker_api import DockerAPI
from ..config.config import Config

class LeaderElectionService:
    def __init__(self, db_client: MongoDBClient, config: Config):
        self.db_client = db_client
        self.config = config
        print("LeaderElectionService Started Up")

    async def attempt_to_elect_leader(self):
        return await self.db_client.elect_leader(self.config.CONTAINER_ID, self.config.LEADER_LEASE_DURATION)

class MonitoringService:
    def __init__(self, docker_api: DockerAPI):
        self.docker_api = docker_api
        print("MonitoringService Started Up")

    def monitor_system(self):
        pass
