import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
cluster = MongoClient("mongodb+srv://tzvri75136:Atulrv2005@mortydb.t0mwlvs.mongodb.net/?retryWrites=true&w=majority")
db = cluster['mortydb']
igerrorlogs_collection = db['igerrorlogs']


def igreel(video):
    url = 'https://downloadgram.org'
    
    try:
        response = requests.post(url, data={'url':video}) 
    except Exception as e:
        towrite1 = {'URL':video, 'ERROR':str(e)}
        igerrorlogs_collection.insert_one(towrite1)
        return 'error'
    

    if 'Please Try Again' in response.text:
            return 'error'
    soup = BeautifulSoup(response.content, 'html.parser')
    for i in soup.find_all('video'):
        return i.source['src']




def igphoto(photo):
    url = 'https://downloadgram.org'
    pics = []
    # try:
    response = requests.post(url, data={'url':photo})
    # except Exception as e:
    #     towrite1 = {'URL':photo, 'ERROR':str(e)}
    #     igerrorlogs_collection.insert_one(towrite1)
    #     pics.append('error')
    #     return pics
        


    if 'Please Try Again' in response.text:
        pics.append('error')
        return pics
    else:
        
        soup = BeautifulSoup(response.content, 'html.parser')
        for i in soup.find_all('a'):
            if i['href'].startswith('https://sco'):
                pics.append(i['href'])
            elif i['href'].startswith('https://instagram'):
                pics.append(i['href'])
                
        return pics

