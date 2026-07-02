from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure

MONGO_DETAILS = "mongodb://localhost:27017"

client = None
database = None

def get_database():
    global client, database
    try:
        if client is None:
            client = AsyncIOMotorClient(MONGO_DETAILS)
            database = client.smarthire
        return database
    except ConnectionFailure:
        print("Failed to connect to MongoDB.")
        return None

async def check_db_connection():
    try:
        db = get_database()
        if db is not None:
            # The ismaster command is cheap and does not require auth.
            await db.command("ismaster")
            print("MongoDB connected successfully!")
    except Exception as e:
        print(f"MongoDB connection error: {e}")
