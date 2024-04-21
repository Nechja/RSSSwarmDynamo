from ..infrastructure.mongodb_client import MongoDBClient
from ..infrastructure.docker_api import DockerConnection
from ..infrastructure.http_client import HttpClient
from ..domain.entities import NodeInfo
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
    def __init__(self, docker_api: DockerConnection, config: Config):
        self.docker_api = docker_api
        self.config = config
        print("MonitoringService Started Up")

    def get_my_ip(self):
        return self.docker_api.get_container_ip(self.config.CONTAINER_ID)

    def get_containers(self):
        return self.docker_api.container_ids()
    
    def get_containers_ips(self):
        containers = self.get_containers()
        ips = []
        current_network_id = self.docker_api.get_network_id(self.config.CONTAINER_ID)
        current_container_long_id = self.docker_api.container_long_id_by_short_id(self.config.CONTAINER_ID)
        for container in containers:
            if container == current_container_long_id:
                continue
            if self.docker_api.is_same_network(container, current_network_id):
                ip_info = self.docker_api.get_container_ip(container)
                if ip_info:
                    for network, network_info in ip_info.items():
                        ip = network_info.get('IPAddress')
                        if ip:
                            ips.append(ip)
        return ips


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


class LeaderHttpService:
    def __init__(self, config: Config, http_client: HttpClient, monitoring_service: MonitoringService):
        self.config = config
        self.http_client = http_client
        self.monitoring_service = monitoring_service
        print("LeaderHttpService Started Up")

    def register_nodes(self, nodes):
        for container in nodes:
            my_ip = self.monitoring_service.get_my_ip()
            leader_info = NodeInfo(ip=my_ip, id=self.config.CONTAINER_ID)
            print(f"Sending leader info to {container}")
            response = self.http_client.post(container, '/leader', leader_info.to_dict())
            print(response)


class FollowerHttpService:
    def __init__(self, config: Config, http_client: HttpClient, monitoring_service: MonitoringService):
        self.config = config
        self.http_client = http_client
        self.monitoring_service = monitoring_service
        print("FollowerHttpService Started Up")

    def register_leader(self, leader):
        my_ip = self.monitoring_service.get_my_ip()
        follower_info = NodeInfo(ip=my_ip, id=self.config.CONTAINER_ID)
        print(f"Sending follower info to {leader}")
        response = self.http_client.post(leader, '/nodes', follower_info.to_dict())
        print(response)