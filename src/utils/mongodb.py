# Van las funciones primitivas de la clase original
from pymongo import MongoClient
import os

client = MongoClient(os.getenv('MONGODB_URI'))
db = client["Notes_bot"]

def find_one(collection_name, search_parameters):
    collection = db[collection_name]
    return collection.find_one(search_parameters)

def update_one(collection_name, search_parameters, new_values):
    collection = db[collection_name]
    return collection.update_one(search_parameters, {'$set': new_values}, upsert=True)

def upsert(collection_name, search):
    collection = db[collection_name]
    return collection.update_one({'_id': search["_id"]}, {'$set': search}, upsert=True)

def collections():
    return db.list_collection_names()

def collection(collection_name):
    return list(db[collection_name].find())

def find_element(collection_name, search={}):
    collection = db[collection_name]
    return list(collection.find(search))

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