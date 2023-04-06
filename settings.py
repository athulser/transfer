from pymongo import MongoClient
cluster = MongoClient("mongodb+srv://tzvri75136:Atulrv2005@mortydb.t0mwlvs.mongodb.net/?retryWrites=true&w=majority")
db = cluster['mortydb']
collection_users = db['test']
subs_collection = db['subscribers']
igerrorlogs_collection = db['igerrorlogs']
codes_collection = db['Accesscodes'] 
redeem_collection = db['redeemcodes']
groups_collection = db['testgroups']
yterrorlogs_collection = db['yterrorlogs']
imgerrorlogs_collection = db['imgerrorlogs']






def cleanmode(chat_id, action):
    groups_collection.update_one({'id':str(chat_id)}, {'$set':{'general.clean_mode':f'{action}'}})
    

def get_updates(chat_id, action):
    groups_collection.update_one({'id':str(chat_id)}, {'$set':{'general.get_updates':f'{action}'}})


def nsfw(chat_id, action):
    groups_collection.update_one({'id':str(chat_id)}, {'$set':{'image.nsfw_filter':f'{action}'}})



def chataction(chat_id, action):
    groups_collection.update_one({'id':str(chat_id)}, {'$set':{f'general.chat_action':f'{action}'}})


def general_progress(chat_id, action):
    groups_collection.update_one({'id':str(chat_id)}, {'$set':{'general.progress_animation':f'{action}'}})

def add_entry(chat_id):
    to_add = {
        'id' : f'{chat_id}',
        'general':{'clean_mode':'off',
                   'get_updates':'on',
                   'chat_action':'on',
                   'progress_animation':'off'
        },
        'play': {'max_results':5},
        'image' : {'nsfw_filter':'on'} 
    }
    groups_collection.insert_one(to_add)
    return '200'
