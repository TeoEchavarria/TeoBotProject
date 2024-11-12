# Van las funciones primitivas de la clase original
from pymongo import MongoClient
import os

client = MongoClient(os.getenv("MONGODB_URI"))
db = client["Notes_bot"]


def create_db_and_collection(mongo_uri, db_name, collection_name):
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]
    return collection


def find_one(collection_name, search_parameters, mongo_key=None):
    if mongo_key is not None:
        client = MongoClient(mongo_key)
        db = client["Notes_bot"]
    else:
        client = MongoClient(os.getenv("MONGODB_URI"))
        db = client["Notes_bot"]
    collection = db[collection_name]
    return collection.find_one(search_parameters)


def update_one(collection_name, search_parameters, new_values):
    collection = db[collection_name]
    return collection.update_one(search_parameters, {"$set": new_values}, upsert=True)


def upsert(collection_name, search, update_data):
    collection = db[collection_name]
    return collection.update_one(search, {"$set": update_data}, upsert=True)


def collections():
    return db.list_collection_names()


def collection(collection_name, mongo_key=None):
    if mongo_key is not None:
        client = MongoClient(mongo_key)
        db = client["Notes_bot"]
    else:
        client = MongoClient(os.getenv("MONGODB_URI"))
        db = client["Notes_bot"]
    return list(db[collection_name].find())


def find_element(collection_name, search={}):
    collection = db[collection_name]
    return list(collection.find(search))


def insert(collection_name, data):
    collection = db[collection_name]
    return collection.insert_one(data)


def exist(collection_name, search_parameters):
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


def add_or_update_key(
    username,
    mongo_key=None,
    owner=None,
    repo=None,
    directory_path=None,
    notes=None,
    pinecone_key=None,
    openai_key=None,
):
    search = {"_id": username}
    update_data = {
        "mongo_key": mongo_key,
        "owner": owner,
        "repo": repo,
        "directory_path": directory_path,
        "notes": notes,
        "pinecone_key": pinecone_key,
        "openai_key": openai_key,
    }
    # Remove any None values, only update provided values
    update_data = {k: v for k, v in update_data.items() if v is not None}

    upsert("users", search, update_data)
