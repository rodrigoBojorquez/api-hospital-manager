from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.environ["DATABASE_HOST"], int(os.environ["DATABASE_PORT"]))
db = client.hospital

db["users"].create_index(["email"], unique=True)
db["users"].create_index(["license_number"], unique=True)