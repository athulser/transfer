from pymongo import MongoClient
cluster = MongoClient("mongodb+srv://tzvri75136:Atulrv2005@mortydb.t0mwlvs.mongodb.net/?retryWrites=true&w=majority")
db = cluster['mortydb']
collection_groups = db['testgroups']
collection_users = db['test']

# 0 is FALSE
# 1 is TRUE

for document in collection_groups.find({}):
    to_write = {
        'id' : f'{document["id"]}',
        'general':{'clean_mode':'off',
                   'get_updates':'on',
                   'chat_action':'on',
                   'progress_animation':'off'
        },
        'play': {'max_results':5},
        'image' : {'nsfw_filter':'on'} 
    }
    collection_groups.update_one({'id':f'{document["id"]}'}, {'$set':to_write})
print("Updated")
    



    




