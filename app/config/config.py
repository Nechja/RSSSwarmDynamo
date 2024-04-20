import os

class Config:
    MONGODB_URI = os.getenv('MONGODB_URI')
    DB_NAME = os.getenv('DB_NAME')
    CONTAINER_ID = os.getenv("CONTAINER_ID", "default_id")
    LEADER_LEASE_DURATION = int(os.getenv('LEADER_LEASE_DURATION', '10'))
    FLASK_PORT = 3333
    print(f"LEADER_LEASE_DURATION: {LEADER_LEASE_DURATION}, CONTAINER_ID: {CONTAINER_ID}, MONGODB_URI: {MONGODB_URI}, DB_NAME: {DB_NAME}")

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
