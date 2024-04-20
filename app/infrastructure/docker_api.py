from docker import DockerClient, APIClient


class DockerConnection:
    def __init__(self):
        self.client = DockerClient.from_env()
        self.api_client = APIClient(base_url='unix://var/run/docker.sock')

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
        containers = self.client.containers.list()
        return [container.id for container in containers]
    
    def container_long_id_by_short_id(self, short_id):
        return self.client.containers.get(short_id).id


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
    
    def get_container_ip(self, container_id):
        try:
            container = self.client.containers.get(container_id)
            return container.attrs['NetworkSettings']['Networks']
        except Exception as e:
            print(f"Error getting IP address for container {container_id}: {e}")
            return None
        
    def get_network_id(self, container_id):
        container_info = self.api_client.inspect_container(container_id)
        for network_name, network_details in container_info['NetworkSettings']['Networks'].items():
            return network_details['NetworkID']
        
    def is_same_network(self, container_id, network_id):
        container_info = self.api_client.inspect_container(container_id)
        for network_name, network_details in container_info['NetworkSettings']['Networks'].items():
            if network_details['NetworkID'] == network_id:
                return True
        return False
