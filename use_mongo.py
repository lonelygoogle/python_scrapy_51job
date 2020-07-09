import pymongo

myclient = pymongo.MongoClient("mongodb://81.68.119.98:27017")
# myclient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myclient['imooc']
mycollection = mydb['pymongo_test']
# mycollection.insert_one({"name": "huangsiqin", "age": "24", "gender": "male"})
# result = mycollection.insert_one({"name": "huangsiqin2", "age": "25", "gender": "male"})
# print(result)
result = mycollection.find({}, {'_id':0}
)
for item in result:
	print(item)