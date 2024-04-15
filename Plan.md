**Step 1: Container Initialization**
- Each container starts and initializes its environment.
- Attempts to elect a leader using `findAndModify` on a specific MongoDB document reserved for leader election.

**Step 2: Leader Election**
- The container checks if there is a current leader by querying the 'leader' document which includes a timestamp.
- If the timestamp is outdated (i.e., the current leader has not updated it within a specific interval), the container attempts to declare itself as the new leader.

**Step 3: Continuous Monitoring (Leader Only)**
- The leader continuously monitors the MongoDB for new or pending tasks.
- Evaluates the workload and current number of active containers.

**Step 4: Scaling Decision (Leader Only)**
- Based on the workload, the leader decides whether to scale up or down.
- Uses Docker API to adjust the number of containers.

**Step 5: Task Assignment**
- The containers independently pull tasks from MongoDB.

**Step 6: Task Processing**
- Each container processes its assigned tasks.
- After completing a task, the container updates the task status in MongoDB.

**Step 7: Completion Check**
- After completing the task, the container checks if more tasks are available.
- If more tasks are present, it repeats from Step 5.
- If no tasks are left and scaling down is appropriate, the container may shut down or go into idle.

**Step 8: Leader Maintenance**
- The leader regularly updates its timestamp in the 'leader' document.
- Continuously checks the system's state and adjusts the scaling as necessary.
- Lets containers know if they can scale back or stay idle for more work.
- The leader would be the last one left running if there is no work, checking and seeing if the tasks in MongoDB set scaling levels.

```
Starting basics:
|-- /app
|   |-- __init__.py
|   |-- /domain
|   |   |-- __init__.py
|   |   |-- entities.py
|   |   |-- services.py
|   |-- /application
|   |   |-- __init__.py
|   |   |-- services.py
|   |-- /infrastructure
|   |   |-- __init__.py
|   |   |-- docker_api.py
|   |   |-- mongodb_client.py
|   |-- /config
|   |   |-- __init__.py
|   |   |-- config.py
|-- main.py
|-- requirements.txt
|-- Dockerfile
|-- docker-compose.yml
```

Notes: container will need to map to: /var/run/docker.sock:/var/run/docker.sock 
