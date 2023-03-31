import requests
from bs4 import BeautifulSoup
import instaloader
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




# def igphoto(photo):
#     url = 'https://downloadgram.org'
#     toreturn = []
#     # try:
#     response = requests.post(url, data={'url':photo})
#     # except Exception as e:
#     #     towrite1 = {'URL':photo, 'ERROR':str(e)}
#     #     igerrorlogs_collection.insert_one(towrite1)
#     #     pics.append('error')
#     #     return pics
        


#     if 'Please Try Again' in response.text:
#         toreturn.append('error')
#         return toreturn
#     else:
        
#         soup = BeautifulSoup(response.content, 'html.parser')
#         for pic in soup.find_all('img'):
#             if pic['src'].startswith('https://imageproxy'):
#                 toreturn.append(pic['src'])

#         for video in soup.find_all('a'):
#              if video['href'].startswith('https://instagram'):
#                 toreturn.append(video['href'])
#         print(toreturn)
#                 # print('video: '+str(video))
#             # if i['href'].startswith('https://sco'):
#             #     pics.append(i['href'])
#             # if i['href'].startswith('https://instagram'):
#             #     pics.append(i['href'])
            




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
            # elif i['href'].startswith('https://instagram'):
            #     toreturn.append('##photo##'+str(i['href']))
        return toreturn

        
# def instagram(username):
   
#     bot = instaloader.Instaloader()
#     profile = instaloader.Profile.from_username(bot.context, username)

#     data = {"userID" : profile.userid,
#             "posts_count" : profile.mediacount,
#             "followers" : profile.followers,
#             "following" : profile.followees,
#             "bio" : profile.biography,
#             "external_url" : profile.external_url,
#             "profile_url" : profile.profile_pic_url, 
#             "full_name" : profile.full_name     
#             }
#     return data
    
        



