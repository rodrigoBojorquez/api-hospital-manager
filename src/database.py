from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.environ["DATABASE_HOST"], int(os.environ["DATABASE_PORT"]))
db = client.hospital

if "email_1" not in db.users.index_information():
    db["users"].create_index("email", unique=True)

if "license_number_1" not in db.users.index_information():
    db["users"].create_index("license_number", unique=True)

# db["users"].create_index(
#     ["email", 
#      "experience.clinic", 
#      "experience.work", 
#      "experience.from_date", 
#      "experience.to_date"],
#      unique=True
# )