import pymongo
 
client = pymongo.MongoClient("localhost", 27017)
db = client.test
db.my_collection.insert_one({"x": 13})

