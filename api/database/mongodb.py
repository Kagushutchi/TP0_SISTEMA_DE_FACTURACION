from pymongo import MongoClient
from api.config import MONGO_URI, MONGO_DATABASE

client = MongoClient(MONGO_URI)
db = client[MONGO_DATABASE]
facturas = db["facturas"]
