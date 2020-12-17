from hdfs import Client
from kafka import KafkaConsumer
from config import *

client_hdfs = Client(hdfs_server)
consumer = KafkaConsumer('big_data_product_topic', bootstrap_servers=kafka_server)
first_time = True
for msg in consumer:
    if first_time:
        client_hdfs.write('product.parquet', data=msg.value, overwrite=True)
        first_time = False
    else:
        data = msg.value()
        client_hdfs.write('product.parquet', data=msg.value, append=True)
