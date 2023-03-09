import json, time, requests, random, openai
import openai, os
from openai.error import RateLimitError, APIError
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
AI_API_KEY = os.getenv('AI_API_KEY')
ERROR500 = 'AI Model is facing a slight traffic at this moment, Please try again after 5 minute.'
FORBIDDEN = 'Your query contains forbidden words/phrases.'
RATELIMIT = 'AI Model is facing high traffic at this moment. Will be recovered in 0-2 hours. Thankyou.'

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
    with open('users.json', 'r') as file:
        json_data = json.load(file)
        for i in json_data:
            i['images_generated'] = 0
            i['messages_generated'] = 0
    with open('users.json', 'w') as file:
        json.dump(json_data, file, indent=4)
        return "200"
    

    
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
    with open('subscribers.json', 'r') as filetoread:
        json_data = json.load(filetoread)
        status = 0
        for i in json_data:
            if i['id'] == str(userID):
                status = 1 # TRUE = 1 AND FALSE = 0
            else:
                status = 0
        return status
    





        



