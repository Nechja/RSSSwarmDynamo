import pymongo
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta

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