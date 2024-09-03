# Van las funciones primitivas de la clase original
from pymongo import MongoClient
import os

client = MongoClient(os.getenv('MONGODB_URI'))
db = client["NotesEmbeddings"]

def upsert(collection_name, search):
    collection = db[collection_name]
    return collection.update_one({'_id': search["_id"]}, {'$set': search}, upsert=True)

def collections():
    return db.list_collection_names()

def collection(collection_name):
    return db[collection_name]

def find_element(collection_name, search={}):
    collection = db[collection_name]
    return list(collection.find(search).sort({'_id': 1}))

def insert(collection_name, data):
    collection = db[collection_name]
    return collection.insert_one(data)

def exist(collection_name,  search_parameters):
    collection = db[collection_name]
    song = collection.find_one(search_parameters)
    return song is not None

def update(collection_name, search_parameters, new_values):
    collection = db[collection_name]
    collection.update_one(search_parameters, new_values)

def delete(collection_name, search_parameters):
    collection = db[collection_name]
    result = collection.delete_many(search_parameters)
    return result.deleted_count