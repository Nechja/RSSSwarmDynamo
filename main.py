from injector import Injector, singleton
from app.infrastructure.mongodb_client import MongoDBClient
from app.infrastructure.docker_api import DockerAPI
from app.application.services import LeaderElectionService, MonitoringService

def configure(binder):
    binder.bind(MongoDBClient, to=MongoDBClient, scope=singleton)
    binder.bind(DockerAPI, to=DockerAPI, scope=singleton)
    binder.bind(LeaderElectionService, to=LeaderElectionService, scope=singleton)
    binder.bind(MonitoringService, to=MonitoringService, scope=singleton)

if __name__ == '__main__':
    injector = Injector(configure)
    leader_service = injector.get(LeaderElectionService)
    monitoring_service = injector.get(MonitoringService)

