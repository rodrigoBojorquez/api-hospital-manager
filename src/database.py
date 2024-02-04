from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.environ("DATABASE_HOST"), os.environ("DATABASE_PORT"))