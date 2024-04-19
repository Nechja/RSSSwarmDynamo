import docker

class DockerAPI:
    def __init__(self):
        self.client = docker.from_env()

    def scale_containers(self, service_name, scale_to):
        service = self.client.services.get(service_name)
        service.scale(scale_to)

    def container_stats(self, container_id):
        container = self.client.containers.get(container_id)
        return container.stats(stream=False)

    def container_logs(self, container_id):
        container = self.client.containers.get(container_id)
        return container.logs()

    def container_ids(self):
        containers = self.client.containers.list(all=True)
        return [container.id for container in containers]

    def count_containers(self):
        containers = self.client.containers.list()
        return len(containers)

    def check_health(self, container_id):
        container = self.client.containers.get(container_id)
        return container.attrs['State']

    def check_resources(self):
        stats = []
        containers = self.client.containers.list()
        for container in containers:
            container_stats = container.stats(stream=False)
            stats.append({
                'id': container.id,
                'cpu_usage': container_stats['cpu_stats']['cpu_usage']['total_usage'],
                'mem_usage': container_stats['memory_stats']
            })
        return stats