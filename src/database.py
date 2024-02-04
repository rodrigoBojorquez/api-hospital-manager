from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.environ["DATABASE_HOST"], int(os.environ["DATABASE_PORT"]))
db = client.hospital

db["patients"].create_index(["email"], unique=True)
db["doctors"].create_index(["email", "license_number"], unique=True)