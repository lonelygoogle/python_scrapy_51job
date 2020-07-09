import pymongo

class Mongo_client(object):
	def __init__(self):
		myclient = pymongo.MongoClient("mongodb://81.68.119.98:27017")
		mydb = myclient['db_51job_m']
		self.mycollection = mydb['collection_51job_m']

	def insert_db(self, item):
		self.mycollection.insert_many(item)


insert_data = Mongo_client()