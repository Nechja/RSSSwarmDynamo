class Task:
    def __init__(self, id, description, status):
        self.id = id
        self.description = description
        self.status = status
        

class Leader:
    def __init__(self, id, last_active):
        self.id = id
        self.last_active = last_active
