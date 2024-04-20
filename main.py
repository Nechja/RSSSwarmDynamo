from app.infrastructure.mongodb_client import MongoDBClient
from app.infrastructure.docker_api import DockerConnection
from app.application.services import LeaderElectionService, MonitoringService, TaskService
from app.config.config import DevelopmentConfig, ProductionConfig, Config
from app.infrastructure.flask_service import FlaskFollowerService
from app.infrastructure.http_client import HttpClient
from app.domain.entities import NodeInfo

import os
import asyncio
import time


if __name__ == '__main__':
    async def main():
        config = DevelopmentConfig() if os.getenv('ENV', 'development') == 'development' else ProductionConfig()
        db_client = MongoDBClient(config.MONGODB_URI, config.DB_NAME)
        leader_election_service = LeaderElectionService(db_client, config)
        monitoring_service = MonitoringService(DockerConnection(), config)
        leader = await leader_election_service.attempt_to_elect_leader()
        httpclient = HttpClient(config)
        if leader:
            print(f"I am the leader starting monitoring service...")
            container_ips = monitoring_service.get_containers_ips()
            time.sleep(15)
            for container in container_ips:
                my_ip = monitoring_service.get_my_ip()
                leader_info = NodeInfo(ip=my_ip, id=config.CONTAINER_ID)
                print(f"Sending leader info to {container}")
                response = httpclient.post(container, '/leader', leader_info.to_dict())
                print(response)


        else:
            print("I am not leader... searching for work to do...")
            flask_service = FlaskFollowerService(config)
            flask_service.run()



    asyncio.run(main())
        


