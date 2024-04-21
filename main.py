from app.infrastructure.mongodb_client import MongoDBClient
from app.infrastructure.docker_api import DockerConnection
from app.application.services import LeaderElectionService, MonitoringService, TaskService, LeaderHttpService, FollowerHttpService
from app.config.config import DevelopmentConfig, ProductionConfig, Config
from app.infrastructure.flask_service import FlaskFollowerService, FlaskLeaderService
from app.infrastructure.http_client import HttpClient
from app.infrastructure.logger_service import LoggerService
from app.domain.entities import NodeInfo

import os
import asyncio
import time


if __name__ == '__main__':
    async def main():
        logger = LoggerService()
        config = DevelopmentConfig() if os.getenv('ENV', 'development') == 'development' else ProductionConfig()
        db_client = MongoDBClient(config.MONGODB_URI, config.DB_NAME)
        leader_election_service = LeaderElectionService(db_client, config)
        monitoring_service = MonitoringService(DockerConnection(), config)
        leader = await leader_election_service.attempt_to_elect_leader()
        httpclient = HttpClient(config)
        
        if leader:
            logger.info(f"I am the leader! {config.CONTAINER_ID}")
            

            container_ips = monitoring_service.get_containers_ips()
            time.sleep(5)
            flask_service = FlaskLeaderService(config, httpclient)
            leader_http_client = LeaderHttpService(config, httpclient, monitoring_service)
            leader_http_client.register_nodes(container_ips)
            flask_service.run()
            


        else:
            logger.info("I am not leader... searching for work to do...")
            follower_http_client = FollowerHttpService(config, httpclient, monitoring_service)
            flask_service = FlaskFollowerService(config, follower_http_client, logger)
            flask_service.run()



    asyncio.run(main())
        


