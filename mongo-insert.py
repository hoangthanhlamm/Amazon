from kafka import KafkaConsumer
import pymongo

from config import *
consumer = KafkaConsumer('big_data_review_topic', bootstrap_servers=kafka_server)


myclient = pymongo.MongoClient(mongo_uri)

mydb = myclient["mydatabase"]
mycol = mydb["review"]


for msg in consumer:
    mycol.insert_one(msg)



