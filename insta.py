import requests
from bs4 import BeautifulSoup
from yt_dlp import YoutubeDL
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

def igreel2(video):
    with YoutubeDL({'quiet':True}) as ydl:
        info = ydl.extract_info(video, download=False)
    return info['formats'][0]['url']


def igphoto(url):
    page = 'https://downloadgram.org'
    toreturn = []
    response = requests.post(page, data={'url':url})
    if 'Please Try Again' in response.text:
        toreturn.append('error')
        return toreturn
    else:
        soup = BeautifulSoup(response.content, 'html.parser')

        # CHECK FOR VIDEOS   
        if soup.find_all('video'):
            for video in soup.find_all('video'):
                videourl = '##video##' + video.source['src']
                toreturn.append(videourl)


        # CHECK FOR PHOTOS
        for i in soup.find_all('a'):
            if i['href'].startswith('https://sco'):
                toreturn.append('##photo##'+str(i['href']))
        return toreturn





