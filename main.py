from app.infrastructure.mongodb_client import MongoDBClient
from app.infrastructure.docker_api import DockerAPI
from app.application.services import LeaderElectionService, MonitoringService, TaskService
from app.config.config import DevelopmentConfig, ProductionConfig, Config
import os
import asyncio


if __name__ == '__main__':
    async def main():
        config = DevelopmentConfig() if os.getenv('ENV', 'development') == 'development' else ProductionConfig()
        db_client = MongoDBClient(config.MONGODB_URI, config.DB_NAME)
        leader_election_service = LeaderElectionService(db_client, config)
        monitoring_service = MonitoringService(DockerAPI())
        leader = await leader_election_service.attempt_to_elect_leader()
        if leader:
            print(f"I am the leader starting monitoring service...")
            monitoring_service.monitor_system()
        else:
            print("I am not leader... searching for work to do...")
            task_service = TaskService(db_client, config)
            tasks = await task_service.start()
            if not tasks:
                print("No tasks found. Reporting in and Going to sleep.")



    asyncio.run(main())
        


