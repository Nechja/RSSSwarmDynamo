from ..infrastructure.mongodb_client import MongoDBClient
from ..infrastructure.docker_api import DockerAPI
from ..config.config import Config
import time

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

class TaskService:
    def __init__(self, db_client: MongoDBClient, config: Config):
        self.config = config
        self.db_client = db_client
        print("Task Service Started Up")

    async def start(self):
        tasks = await self.db_client.check_for_work()
        if not tasks:
            print("No tasks found.")
            return None
        if tasks:
            print(f"Found {len(tasks)} tasks to do.")
            for task in tasks:
                print(f"Challanging task {task['name']}")
                challange = await self.checkout_task(task)
                print(challange)
                if challange:
                    print(f"Challanged task {task['name']}")
                    await self.run_task(task)
                    break

            print("winding into next task...")
            await self.start()


        
    
    async def checkout_task(self, task):
        return await self.db_client.checkout_task(task, self.config.CONTAINER_ID)
        

    async def run_task(self, task):
        time.sleep(30)
        print(f"Task {task['name']} completed.")


