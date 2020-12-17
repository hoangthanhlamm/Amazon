import os

kafka_server = os.environ.get('KAFKA_SERVER', 'localhost:9092')
hdfs_server = os.environ.get('HDFS_SERVER', 'http://hadoop-master:50070')
mongo_uri = os.environ.get('MONGO_URI', "mongodb://localhost:27017/")
