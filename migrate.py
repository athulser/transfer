from pymongo import MongoClient
import datetime
cluster = MongoClient("mongodb+srv://tzvri75136:Atulrv2005@mortydb.t0mwlvs.mongodb.net/?retryWrites=true&w=majority")
db = cluster['mortydb']
collection_users = db['users']
collection_redeem = db['redeemcodes']


collection_users.update_many({}, {'$unset':{"messages_generated":1, "images_generated":1}})
print("Removed!")
collection_users.update_many({}, {'$set':{"credits":3, "joinedOn":datetime.datetime.now().timestamp()}})
print("Updated!")



# collection_redeem.insert_one({"code":"31ybpykrju45vcaads7k", "credits":3})
# collection_redeem.insert_one({"code":"rlqh42hj00er5nvi7u56", "credits":3})
# collection_redeem.insert_one({"code":"qrh316d9uxczru9tcmd1", "credits":7})
# collection_redeem.insert_one({"code":"k1dpeamw6f59ffx61ml2", "credits":16})

