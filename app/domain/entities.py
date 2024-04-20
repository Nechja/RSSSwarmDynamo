from enum import Enum

class Occurance(Enum):
    ONCE = 1
    HOURLY = 2
    DAILY = 3
    WEEKLY = 4

class Status(Enum):
    PENDING = 1
    RUNNING = 2
    COMPLETED = 3
    FAILED = 4


class Task:
    def __init__(self, id, name, status: Status, action, occurance: Occurance, assignee=None, last_run=None):
        self.id = id
        self.name = name
        self.action = action 
        self.occurance = occurance
        self.assignee = assignee
        self.status = status
        self.lastrun = last_run

class Leader:
    def __init__(self, id, last_active):
        self.id = id
        self.last_active = last_active

class NodeInfo:
    def __init__(self, id, ip):
        self.id = id
        self.ip = ip

    def to_dict(self):
        return {
            'id': self.id,
            'ip': self.ip
        }


