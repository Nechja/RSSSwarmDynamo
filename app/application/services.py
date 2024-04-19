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

    def report_container_health(self):
        container_ids = self.docker_api.container_ids()
        health_status = {container_id: self.docker_api.check_health(container_id) for container_id in container_ids}
        print(health_status)
        return health_status

    def report_container_resources(self):
        return self.docker_api.check_resources()

    def alert_high_resource_usage(self, cpu_threshold=80, memory_threshold=80):
        resources = self.docker_api.check_resources()
        print(resources)

    def monitor_containers(self):
        import time
        try:
            while True:
                print("Reporting Container Health")
                print(self.report_container_health())
                print("Reporting Resource Usage")
                print(self.report_container_resources())
                self.alert_high_resource_usage()
                time.sleep(60)  
        except KeyboardInterrupt:
            print("Monitoring stopped by user.")


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


