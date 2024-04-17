import pymongo
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta
from ..domain.entities import Occurance

class MongoDBClient:
    def __init__(self, db_uri, db_name):
        self.client = AsyncIOMotorClient(db_uri)
        self.db = self.client[db_name]
        print(f"Connected to MongoDB database {db_name}")

    def test_connection(self):
        try:
            info = self.client.server_info()
            print(f'Connected to MongoDB server {info["version"]}')
            return True
        except pymongo.errors.ServerSelectionTimeoutError:
            return False

    async def elect_leader(self, container_id, lease_duration):
        print('Electing leader...')
        collection = self.db['Leader']
        now = datetime.now()
        lease_expires = now + timedelta(seconds=lease_duration)
        try:
            result = await collection.find_one_and_update(
                {   
                    '_id': 'leader_doc',
                    '$or': [
                        {'leader_id': None}, 
                        {'lease_expires': {'$lte': now}}
                    ]
                },
                {
                    '$set': {
                        'leader_id': container_id,
                        'lease_expires': lease_expires
                    }
                },
                upsert=True,
                return_document=pymongo.ReturnDocument.AFTER
            )
            return result
        except pymongo.errors.DuplicateKeyError:
            print(f"{container_id} has failed to update leader document. Another container is the leader.")
            return None
        except Exception as e:
            print(f'Error electing leader: {e}')
            return None

    async def check_for_work(self):
        print("Checking for available tasks...")
        collection = self.db['Tasks']
        now = datetime.now()
        result = await collection.find({
            '$or': [
                {'assignee': None}, 
                {'lastrun': {'$exists': False}}, 
                {'occurance': Occurance.ONCE.value, 'lastrun': {'$exists': True}}, 
                {'occurance': Occurance.HOURLY.value, 'lastrun': {'$lt': now - timedelta(hours=1)}},
                {'occurance': Occurance.DAILY.value, 'lastrun': {'$lt': now - timedelta(days=1)}},
                {'occurance': Occurance.WEEKLY.value, 'lastrun': {'$lt': now - timedelta(weeks=1)}}
            ]
        }).to_list(None)
        return result
    
    async def checkout_task(self, task, assignee):
        print(f"Checking out task {task['name']}...")
        collection = self.db['Tasks']
        try:
            result = await collection.find_one_and_update(
                {
                    'name': task['name'],
                    'assignee': None  
                },
                {
                    '$set': {
                        'assignee': assignee,
                        'status': 'InProgress' 
                    }
                },
                return_document=pymongo.ReturnDocument.AFTER
            )
            if result:
                print(f"Task {result['name']} checked out by {assignee}.")
                return result
            else:
                print(f"Task {task['name']} is already checked out or does not exist.")
                return None
        except pymongo.errors.DuplicateKeyError:
            print(f"{assignee} has failed to check out task {task['name']}.")
            return None
        except Exception as e:
            print(f'Error on task assingment {e}')
            return None
        return result
