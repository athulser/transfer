import json, time, requests, random, openai
import openai, os
import pymongo
from pymongo import MongoClient
from openai.error import RateLimitError, APIError
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
AI_API_KEY = os.getenv('AI_API_KEY')
ERROR500 = 'AI Model is facing a slight traffic at this moment, Please try again after 5 minute.'
FORBIDDEN = 'Your query contains forbidden words/phrases.'
RATELIMIT = 'AI Model is facing high traffic at this moment. Will be recovered in 0-2 hours. Thankyou.'
cluster = MongoClient("mongodb+srv://tzvri75136:Atulrv2005@mortydb.t0mwlvs.mongodb.net/?retryWrites=true&w=majority")
db = cluster['mortydb']
subs_collection = db['subscribers']
collection_users = db['users']
collection_codes = db['Accesscodes']


with open('users.json') as users:
    json_data_users = json.load(users)
    for i in json_data_users:
        collection_users.insert_one(i)
    print("Users data migrated")
        

with open('subscribers.json', 'r') as subs:
    json_data_subs = json.load(subs)
    for i in json_data_subs:
        subs_collection.insert_one(i)
    print("Subscribers data migrated")

with open('Accesscodes.json', 'r') as codes:
    json_data_codes = json.load(codes)
    for i in json_data_codes:
        collection_codes.insert_one(i)
    print("Codes data migrated")



def askAI(text):
    openai.api_key = AI_API_KEY
    try:
        response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages =[
            {"role": "system", "content": text}
        ],
        temperature = 0.5,
        max_tokens = 99)
        return response['choices'][0]['message']['content'].strip()
    except RateLimitError:
        print("RATE LIMIT REACHED")
        return 'ratelimit'
    except APIError:
        print("500 SERVER ERROR")
        return '500'
    except Exception as e:
        data = f'QUERY : {text}\n{e}\nTRACEBACK\n\n{e.with_traceback}\n\n---------------------\n\n'
        with open('msgErrorLog.txt', 'a', encoding='utf-8') as f:
            f.write(data)
            print("ERROR HAS BEEN LOGGED")



def resetFile():
    collection_users.update_many({}, {'$set':{"images_generated":0, "messages_generated":0}})
    return '200'
    

    
def isValid(link):
    if link.startswith('https://youtu.be/'):
        return True
    else:
        return False
    



def sourcecode(url):
    try:
        start = time.time()
        r = requests.get(url)
        end = time.time()
        time_taken = round(end) - round(start)
        if time_taken > 4:
            return 'timeout'
        else :
            return r.text
    except requests.exceptions.ConnectionError:
        return 'err'
    



def randomNumber():
    num = random.randint(1000, 9999)
    return num


def isSubscriber(userID):
    status = 0
    res = subs_collection.find_one({"id":str(userID)})
    if res:
        status = 1
    else:
        status = 0

    return status
    





        



