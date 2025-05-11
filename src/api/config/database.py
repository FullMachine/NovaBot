from motor.motor_asyncio import AsyncIOMotorClient
from src.utils.logger import setup_logger
import os
from dotenv import load_dotenv
from .settings import settings

# Load environment variables
load_dotenv()

logger = setup_logger("database", "api.log")

class Database:
    client: AsyncIOMotorClient = None
    database_name = os.getenv("DATABASE_NAME", "nova_sports")

    @classmethod
    async def connect_db(cls):
        try:
            cls.client = AsyncIOMotorClient(settings.DATABASE_URL)
            logger.info("Connected to MongoDB.")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise e

    @classmethod
    async def close_db(cls):
        try:
            if cls.client:
                cls.client.close()
                logger.info("Closed MongoDB connection.")
        except Exception as e:
            logger.error(f"Error closing MongoDB connection: {e}")
            raise e

    @classmethod
    def get_db(cls):
        return cls.client[cls.database_name]

async def get_database():
    client = AsyncIOMotorClient(settings.DATABASE_URL)
    return client[settings.DATABASE_NAME]

async def close_database(client):
    if client:
        client.close() 