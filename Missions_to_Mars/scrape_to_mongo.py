# Dependencies
import pymongo
import datetime
import scrape_mars

# The default port used by MongoDB is 27017

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# Declare the database
db = client.mars_db

# Declare the collection
collection = db.mars_info

db.collection.drop

scrape_var = scrape_mars.scrape()

db.collection.insert_many([scrape_var])