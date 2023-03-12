import openai, telebot, datetime, os, time, re, requests, threading
from yt_dlp import YoutubeDL
from pymongo import MongoClient
from youtube_search import YoutubeSearch
from functions import askAI, resetFile, sourcecode, isValid, randomNumber, isSubscriber, json, FORBIDDEN, ERROR500, RATELIMIT
from dotenv import load_dotenv, find_dotenv
from openai.error import RateLimitError, InvalidRequestError, APIError
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
telebot.apihelper.READ_TIMEOUT = 60
load_dotenv(find_dotenv())
TELE_API_KEY = os.getenv('TELE_API_KEY')
AI_API_KEY = os.getenv('AI_API_KEY')
SUDO_ID = os.getenv('SUDO_ID')


cluster = MongoClient("mongodb+srv://tzvri75136:Atulrv2005@mortydb.t0mwlvs.mongodb.net/?retryWrites=true&w=majority")
db = cluster['mortydb']
collection_users = db['users']
subs_collection = db['subscribers']
codes_collection = db['Accesscodes']


# INITIALISING THE BOT WITH TELEGRAM API
bot = telebot.TeleBot(TELE_API_KEY, threaded=True)
openai.api_key = AI_API_KEY
active_users = {}



# FUNCTION TO SEARCH VIDEO AND RETURN DICTIONARY OF TITLE AND CORRESPONDING URL
def searchVideo(title):
    data = {}
    resultsvid = YoutubeSearch(title, max_results=10).to_dict()
    for i in resultsvid[0:]:
        data.update({f'{i["title"]}':f'{i["url_suffix"]}'})
    return data
        
    
def time_difference(last):
    current_time = datetime.datetime.now().timestamp()
    if (current_time - last) > 60:
        return True
    else:
        return False 



def generate_image(prompt, message):
    num_image = 1
    output_format='url'
    size='1024x1024'
    invalid_words = ['nood','without clothes','girl without','bare body','stab','cum','aunty','girlfriend','sister','handjob','licking','milf','hentai','donald','trump','sex','seduc','dwayne','clevage','girl wearing','fuk','pussy','horny','no clothes','suck','copulation','twerking','scarlett','fck','narendra','gangbang','intercourse','stepmom','stepsister','xxx','xnxx','whore','ass','hot girl','underwear','girl bathing','xi jingping','modi','brazzers','biden','joe','salman','porn','doggy','mia khalifa','sunny leone','bathing','hot girl','inner','inner wear','nanked','sexy','boob', 'leah gotti','nipple','kiss','fuck', 'dick', 'sex','asshole', 'vagina', 'naked','penis', 'butt','breast','chest','naced','abdomen','making out','tits','flirting','firting', 'nude', 'titty', 'titties','poop']
    for i in invalid_words:
        if i in prompt.lower():
            bot.send_message(message.chat.id, "Your query contains forbidden words")
            return 'err'
    try:
        images = []
        response = openai.Image.create(
            prompt=prompt,
            n=num_image,
            size=size,
            response_format=output_format
        )
        if output_format == 'url':
            for image in response['data']:
                images.append(image.url)
        elif output_format == 'b64_json':
            images.append(image.b64_json)
        return {'created':datetime.datetime.fromtimestamp(response['created']), 'images':images}
    except RateLimitError:
        return 'ratelimit'
    except InvalidRequestError:
        return 'forbidden'
    except APIError:
        return '500'
    except Exception as e:
        with open('imgErrorLog.txt', 'a') as file:
            data = f'QUERY : {prompt}\n\n{e}\nTRACEBACK\n\n{e.with_traceback}\n\n---------------------\n\n'
            file.write(data)
            print("ERROR HAS BEEN LOGGED TO FILE")
            bot.send_message(message.chat.id, e)
            return 'err'



# /START COMMAND
@bot.message_handler(commands=['start'])
def start_message(message):
    userID = message.chat.id
    usermsg = message.message_id
    bot.delete_message(chat_id=userID, message_id=usermsg)
    bot.send_message(userID, "Morty AI Bot is a chatbot that provides a range of AI-driven services to help people manage their day-to-day tasks. It can help you with tasks such as:\n\n🔰 *AI Image generation*\n🔰 *AI ChatBot*\n🔰 *Youtube video/audio downloading*\n🔰 *Music player*\n🔰 *Web scraping*\n🔰 *and more.*\n\nIt is powered by *natural language processing (NLP)* and *machine learning technology* to provide a personalized experience. To get started, simply send a message to Morty AI and it will respond with the help you need.\n\n*⚠️ BASIC COMMANDS ⚠️*\n/play - To play any music\n/img - To generate images based on your query\n/msg - Chat with Morty AI\n/youtube - Download YouTube video/audio\n/subscribe - Subscribe to premium\n/scrape - Web scraping\n/join - Join our basements\ndeveloper - Developer Information", parse_mode='Markdown', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("❌ Close ❌", callback_data='close')))
    res = collection_users.find_one({"id":str(userID)})
    if not res:
        towrite = {'id':str(userID), 'images_generated':0, 'messages_generated':0}
        collection_users.insert_one(towrite)
    
@bot.message_handler(['data'])
def data(message):
    if str(message.chat.id) == SUDO_ID:
        for i in codes_collection.find({}):
            bot.send_message(int(SUDO_ID), i['code'])
    



@bot.message_handler(commands=['join'])
def join(message):
    markupjoin = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Join support group", url="https://t.me/+_FoaeZ-tvIQ4OGE9"), InlineKeyboardButton("Join official channel", url="https://t.me/mortylab"), InlineKeyboardButton("🗿 Join Men's Gang 🗿", callback_data="checkpremium"))
    bot.send_message(message.chat.id, "Get support from here", reply_markup=markupjoin)




# /PLAY COMMAND
@bot.message_handler(commands=['play'])
def play_command(message):
    id = message.chat.id
    query = message.text.replace('/play','')
    if len(query) == 0:
        bot.send_message(id, "Use in `/play songname` format\nExample:\n\n`/play intentions`", parse_mode="Markdown")
    else:
        if 'movie' in query.lower() or 'cinema' in query.lower() or 'film' in query.lower() or 'full movie' in query.lower() or '2023' in query.lower():
            bot.send_message(id, "Stop trying to download movies bro...", parse_mode="Markdown")
        else:
            bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            _message = bot.send_message(id, "⌛️", parse_mode='Markdown')
            chat_id, message_id = _message.chat.id, _message.message_id
            dictdata = searchVideo(query)
            first_markup = InlineKeyboardMarkup()
            for title, urlsuffix in dictdata.items():
                urlwithhehe = 'hehe'+ urlsuffix
                first_markup.add(
                    InlineKeyboardButton(title, callback_data=urlwithhehe)
                )
            first_markup.add(
                InlineKeyboardButton("❌ Cancel ❌", callback_data="close")
            )
            bot.edit_message_text(message_id=message_id,chat_id=chat_id, text=f"*Found {str(len(dictdata))} results for {query} 🔎*\n\n👇", reply_markup=first_markup, parse_mode="Markdown")
        



# CALLBACK QUERY HANDLERS FOR ALL COMMANDS WITH INLINEKEYBOARD CALLBACKS
@bot.callback_query_handler(func=lambda message: True)
def callback_query_handler(call):
    if call.data.startswith('hehe'):
        if isSubscriber(call.message.chat.id) == 0:
            now = datetime.datetime.now().timestamp()
            if call.message.chat.id in active_users:
                if time_difference(active_users[call.message.chat.id]):
                    active_users[call.message.chat.id] = now
                else:
                    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                    bot.send_message(chat_id=call.message.chat.id, parse_mode="Markdown", text="*Downloads are limited to 1 download per 60 seconds* (%ds remaining)\n\n/subscribe to get rid of rate limits :)"%(60-(now - active_users[call.message.chat.id])))
                    return
            else:
                active_users[call.message.chat.id] = now
        def fn():
            playurl = 'https://youtube.com'+call.data.replace('hehe','')
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            _message = bot.send_message(chat_id=call.message.chat.id, text="*STATUS* : _Fetching streams_", parse_mode="Markdown")
            html = requests.get(playurl).text
            titleplay = re.findall(r"<title>(.*?)</title>", html)[0]
            authorplay = re.findall(r"\"author\":\"(.*?)\"", html)[0]
            viewsplay = re.findall(r"\"viewCountText\":{\"simpleText\":\"(.*?)\"", html)[0]
            published_onplay = re.findall(r"\"dateText\":{\"simpleText\":\"(.*?)\"", html)[0]
            filename = f'play-{str(randomNumber())}'
            ydl_opts = {
                'format':'bestaudio[ext=mp3]/best',
                'noplaylist':True,
                'outtmpl': filename,
                'geo_bypass':True,
                'prefer_ffmpeg':True,
                'nocheckcertificate':True,
                "quiet":True,
                "postprocessors":[{'key':'FFmpegExtractAudio',
                                   'preferredcodec':'mp3',
                                   'preferredquality':'192'}],
            }

        
            with YoutubeDL(ydl_opts) as ydl:
                bot.edit_message_text(chat_id=_message.chat.id, message_id=_message.message_id, text="*STATUS* : _Downloading in progress_", parse_mode="Markdown")
                try:
                    ydl.download(playurl)
                    bot.edit_message_text(chat_id=_message.chat.id, message_id=_message.message_id, text="*STATUS* : _Download complete_", parse_mode="Markdown")
                except Exception as e:
                    bot.edit_message_text(chat_id=_message.chat.id, message_id=_message.message_id, text="`❗️ Exception occured`", parse_mode="Markdown")
                    data = f'ERROR WHILE DOWNLOADING URL\n\nURL : {playurl}\n{e}\nTRACEBACK\n\n{e.with_traceback}\n\n---------------------\n\n'
                    with open('ytErrorLog.txt', 'a', encoding='utf-8') as file:
                        file.write(data)
                        bot.send_message(call.message.chat.id, "❗️ ERROR HAS BEEN LOGGED")



            # PHASE 2        
            try:
                bot.send_chat_action(chat_id=call.message.chat.id, action="upload_audio")
                bot.edit_message_text(chat_id=_message.chat.id, message_id=_message.message_id, text='⌛️')
                if os.path.getsize(filename+'.mp3') >= 50000000:
                    bot.send_message(chat_id=call.message.chat.id, text="The filesize is too large! Subscribe to premium to get rid of restrictions!")
                    bot.delete_message(chat_id=_message.chat.id, message_id=_message.message_id)
                else:
                    markupclose = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("❌ Close player ❌", callback_data="close"))
                    caption = f'{titleplay} | {authorplay}\n\n*Views* : {viewsplay}\n*Author* : {authorplay}\n*Published on* : {published_onplay}\n\n\n[Morty AI](https://t.me/morty_ai_bot)'
                    with open(filename+'.mp3', 'rb') as audiofile:
                        bot.send_audio(chat_id=call.message.chat.id,audio=audiofile, performer=authorplay, title=titleplay, caption=caption, parse_mode='Markdown', reply_markup=markupclose)
                        bot.delete_message(chat_id=_message.chat.id, message_id=_message.message_id)

            except Exception as n:
                bot.edit_message_text(chat_id=_message.chat.id, message_id=_message.message_id, text="❗️ ERROR WHILE SENTING")
                data2 = f'ERROR WHILE SENTING IN /PLAY\n\nURL : {playurl}\n{n}\n\n---------------------\n\n'
                with open('ytErrorLog.txt', 'a', encoding='utf-8') as file:
                    file.write(data2)
                    bot.send_message(call.message.chat.id, "❗️ ERROR HAS BEEN LOGGED")


            #PHASE 3
            try:
                os.remove(filename+'.mp3')
            except:
                print("ERROR WHILE DELETING")
            newmarkup = InlineKeyboardMarkup(row_width=1)
            newmarkup.add(
                InlineKeyboardButton("Feedback", callback_data='feedback'),
                InlineKeyboardButton("Close", callback_data="close"))
            bot.send_message(call.message.chat.id, "_Mind giving me a feedback?_", parse_mode="Markdown", reply_markup=newmarkup)
        

        threading.Thread(target=fn).start()
       
    


    elif call.data == 'feedback':
        newwmarkup = InlineKeyboardMarkup(row_width=1)
        newwmarkup.add(
            InlineKeyboardButton("Click here", url='https://t.me/dailychannelsbot?start=morty_ai_bot'),
            InlineKeyboardButton("Close", callback_data="close"))
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=newwmarkup)

    elif call.data == 'close':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    elif 'video' in call.data:
        payloadvideo = call.data.replace('video', '').strip()
        markup = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("High Resolution", callback_data=f"highres{payloadvideo}"), InlineKeyboardButton("Low resolution", callback_data=f"lowres{payloadvideo}"), InlineKeyboardButton("﹤﹤ Back", callback_data=f"home{payloadvideo}"))
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)
    elif call.data == 'checkpremium':
        if isSubscriber(call.message.chat.id) == 1:
            submarkup = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Join soldier 💪", url="https://t.me/+HV8y_vKK99djZTBl"), InlineKeyboardButton("Cancel", callback_data="close"))
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=submarkup)
        else:
            dosubmarkup = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("👑 Subscribe 👑", url='https://paypal.me/mortylabz/3USD'), InlineKeyboardButton("Cancel", callback_data="close"))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="*Subscribe to join our Men's premium gang with all the benefits 🗿☕️*",parse_mode="Markdown", reply_markup=dosubmarkup)
    
    elif 'highres' in call.data:
        if isSubscriber(call.message.chat.id) == 0:
            now = datetime.datetime.now().timestamp()
            if call.message.chat.id in active_users:
                if time_difference(active_users[call.message.chat.id]):
                    active_users[call.message.chat.id] = now
                else:
                    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                    bot.send_message(chat_id=call.message.chat.id, parse_mode="Markdown", text="*Downloads are limited to 1 download per 60 seconds* (%ds remaining)\n\n/subscribe to get rid of rate limits :)"%(60-(now - active_users[call.message.chat.id])))
                    return
            else:
                active_users[call.message.chat.id] = now

        def fnhigh():
            youtubevideourl = 'https://youtu.be/'+ call.data.replace("highres", '').strip()
            _message = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="*STATUS* : _Fetching streams_", parse_mode="Markdown")
            filenamevideo = f'videohigh-{str(randomNumber())}'
            ydl_optsvideo = {
                "format":"bestvideo[ext=ogg]+bestaudio[ext=mp3]/best",
                "outtmpl":filenamevideo+'.ogg',
                "geo_bypass":True,
                "quiet":True,
            }
            with YoutubeDL(ydl_optsvideo) as ydl:
                bot.edit_message_text(chat_id=_message.chat.id, message_id=_message.message_id, text="*STATUS* : _Downloading in progress_", parse_mode="Markdown")
                try:
                    ydl.download(youtubevideourl) 
                    bot.edit_message_text(chat_id=_message.chat.id, message_id=_message.message_id, text="*STATUS* : _Download complete_", parse_mode="Markdown")              
                except Exception as e:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="`❗️ Exception occured`", parse_mode="Markdown")
                    data = f'ERROR WHILE DOWNLOADING VIDEO\n\nURL : {youtubevideourl}\n{e}\nTRACEBACK\n\n{e.with_traceback}\n\n---------------------\n\n'
                    with open('ytErrorLog.txt', 'a', encoding='utf-8') as file:
                        file.write(data)
                        bot.send_message(call.message.chat.id, "❗️ ERROR HAS BEEN LOGGED")
                try:
                    
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='⌛️')
                    if os.path.getsize(filenamevideo+'.ogg') >= 50000000:
                         bot.send_message(call.message.chat.id, "Filesize is too large! Subscribe to premium to remove restrictions!")
                         bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                    else:
                        try:
                            html = requests.get(youtubevideourl).text
                            title = re.findall(r"<title>(.*?) - YouTube</title>", html)[0]
                        except:
                            title = 'Downloaded by Morty AI'

                        with open(filenamevideo+'.ogg', 'rb') as videofile:
                            bot.send_chat_action(call.message.chat.id, action="upload_video")
                            bot.send_video(chat_id=call.message.chat.id, video=videofile, caption=f"{title}\n\n[Morty AI](https://t.me/morty_ai_bot)", parse_mode="Markdown")
                            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

                except Exception as q:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="❗️ ERROR WHILE SENTING")
                    data3 = f'ERROR WHILE SENTING VIDEO\n\nURL : {youtubevideourl}\n{q}\nTRACEBACK\n\n{q.with_traceback}\n\n---------------------\n\n'
                    with open('ytErrorLog.txt', 'a', encoding='utf-8') as file:
                        file.write(data3)
                        bot.send_message(call.message.chat.id, "❗️ ERROR HAS BEEN LOGGED")

                try:
                    os.remove(filenamevideo+'.ogg')
                except:
                    print("ERROR WHILE DELETING")

        threading.Thread(target=fnhigh).start()
        


    elif 'audiores' in call.data:
        payloadaudio = call.data.replace('audiores', '').strip()
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Highest quality", callback_data=f"dwaudio{payloadaudio}"), InlineKeyboardButton("﹤﹤ Back", callback_data=f"home{payloadaudio}")))

    elif 'lowres' in call.data:
        if isSubscriber(call.message.chat.id) == 0:
            now = datetime.datetime.now().timestamp()
            if call.message.chat.id in active_users:
                if time_difference(active_users[call.message.chat.id]):
                    active_users[call.message.chat.id] = now
                else:
                    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                    bot.send_message(chat_id=call.message.chat.id, parse_mode="Markdown", text="*Downloads are limited to 1 download per 60 seconds* (%ds remaining)\n\n/subscribe to get rid of rate limits :)"%(60-(now - active_users[call.message.chat.id])))
                    return
            else:
                active_users[call.message.chat.id] = now


        def fnlow():
            youtubevideourl = 'https://youtu.be/'+call.data.replace("lowres", '').strip()
            _message = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="*STATUS* : _Fetching streams_", parse_mode="Markdown")
            filenamevideolow = f'videolow-{str(randomNumber())}'
            ydl_optsvideolow = {
                "format":"worstvideo[ext=mp4]+worstaudio[ext=m4a]/worst",
                "outtmpl":filenamevideolow,
                "geo_bypass":True,
                "quiet":True,
            }
            with YoutubeDL(ydl_optsvideolow) as ydl:
                bot.edit_message_text(chat_id=_message.chat.id, message_id=_message.message_id, text="*STATUS* : _Downloading in progress_", parse_mode="Markdown")
                try:
                    ydl.download(youtubevideourl)
                    bot.edit_message_text(chat_id=_message.chat.id, message_id=_message.message_id, text="*STATUS* : _Download complete_", parse_mode="Markdown")
                except Exception as e:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="`❗️ Exception occured`", parse_mode="Markdown")
                    data5 = f'ERROR WHILE DOWNLOADING LOW VIDEO URL\n\nURL : {youtubevideourl}\n{e}\nTRACEBACK\n\n{e.with_traceback}\n\n---------------------\n\n'
                    with open('ytErrorLog.txt', 'a', encoding='utf-8') as file:
                        file.write(data5)
                        bot.send_message(call.message.chat.id, "❗️ ERROR HAS BEEN LOGGED")  
                try:
                    bot.send_chat_action(chat_id=call.message.chat.id, action="upload_video")
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='⌛️')
                    if os.path.getsize(filenamevideolow+'.mp4') >= 50000000:
                        bot.send_message(call.message.chat.id, "The filesize is too large! Subscribe to premium to get of restrictions!")
                    else:
                        try:
                            html = requests.get(youtubevideourl).text
                            title = re.findall(r"<title>(.*?) - YouTube</title>", html)[0]
                        except:
                            title = 'Downloaded by Morty AI'
                        with open(filenamevideolow+'.mp4', 'rb') as videofile:
                            bot.send_video(chat_id=call.message.chat.id,video=videofile,  caption=f"{title}")
                            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

                except Exception as q:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="❗️ ERROR WHILE SENTING")
                    data6 = f'ERROR WHILE SENTING LOW VIDEO\n\nURL : {youtubevideourl}\n{q}\nTRACEBACK\n\n{q.with_traceback}\n\n---------------------\n\n'
                    with open('ytErrorLog.txt', 'a', encoding='utf-8') as file:
                        file.write(data6)
                        bot.send_message(call.message.chat.id, "❗️ ERROR HAS BEEN LOGGED")

                try:
                    os.remove(filenamevideolow+'.mp4')
                except:
                    print("ERROR WHILE DELETING")
        threading.Thread(target=fnlow).start()


    elif "home" in call.data:
        homepayload = call.data.replace("home", '').strip()
        homemarkup = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton("Video 📹", callback_data=f"video{homepayload}"), InlineKeyboardButton("Audio 🎧", callback_data=f"audiores{homepayload}"), InlineKeyboardButton("❌ Cancel ❌", callback_data="close"))
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=homemarkup)
    elif 'dwaudio' in call.data:
        if isSubscriber(call.message.chat.id) == 0:
            now = datetime.datetime.now().timestamp()
            if call.message.chat.id in active_users:
                if time_difference(active_users[call.message.chat.id]):
                    active_users[call.message.chat.id] = now
                else:
                    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                    bot.send_message(chat_id=call.message.chat.id, parse_mode="Markdown", text="*Downloads are limited to 1 download per 60 seconds* (%ds remaining)\n\n/subscribe to get rid of rate limits :)"%(60-(now - active_users[call.message.chat.id])))
                    return
            else:
                active_users[call.message.chat.id] = now

        def fnaudio():
            youtubevideourl = 'https://youtu.be/'+call.data.replace('dwaudio', '').strip()
            filenameaudio = f'audiohigh-{str(randomNumber())}'
            _message = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="*STATUS* : _Fetching streams_",parse_mode='Markdown')
            ydl_opts = {
                'format':'bestaudio[ext=mp3]/best',
                'noplaylist':True,
                'outtmpl': filenameaudio,
                'geo_bypass':True,
                'prefer_ffmpeg':True,
                'nocheckcertificate':True,
                "quiet":True,
                "postprocessors":[{'key':'FFmpegExtractAudio',
                                   'preferredcodec':'mp3',
                                   'preferredquality':'192'}],
            }
            with YoutubeDL(ydl_opts) as ydl:
                bot.edit_message_text(chat_id=_message.chat.id, message_id=_message.message_id, text="*STATUS* : _Downloading in progress_", parse_mode="Markdown")
                try:
                    ydl.download(youtubevideourl)
                    bot.edit_message_text(chat_id=_message.chat.id, message_id=_message.message_id, text="*STATUS* : _Download complete_", parse_mode="Markdown")
                except Exception as e:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="`❗️ Exception occured`", parse_mode="Markdown")
                    data = f'ERROR WHILE DOWNLOADING AUDIO\n\nURL : {youtubevideourl}\n{e}\nTRACEBACK\n\n{e.with_traceback}\n\n---------------------\n\n'
                    with open('ytErrorLog.txt', 'a', encoding='utf-8') as file:
                        file.write(data)
                        bot.send_message(call.message.chat.id, "❗️ ERROR HAS BEEN LOGGED")

                try:
                    bot.send_chat_action(chat_id=call.message.chat.id, action="upload_audio")
                    try:
                        html2 = requests.get(youtubevideourl).text
                        titleaudio = re.findall(r"<title>(.*?)</title>", html2)[0]
                    except:
                        titleaudio = 'Downloaded by Morty AI'

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='⌛️')
                    if os.path.getsize(filenameaudio+'.mp3') >= 50000000:
                        bot.send_message(call.message.chat.id, "The filesize is too large! Subscribe to premium to get of restrictions!")
                    else:
                        caption = f'{titleaudio}\n\nDownloaded by [Morty AI](https://t.me/morty_ai_bot)'
                        with open(filenameaudio+'.mp3', 'rb') as audiofile:
                            bot.send_audio(chat_id=call.message.chat.id,audio=audiofile, caption=caption, parse_mode='Markdown')
                            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                except Exception as n:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="❗️ ERROR WHILE SENTING")
                    data2 = f'ERROR WHILE SENTING YOUTUBE AUDIO\n\nURL : {youtubevideourl}\n{n}\nTRACEBACK\n\n{n.with_traceback}\n\n---------------------\n\n'
                    with open('ytErrorLog.txt', 'a', encoding='utf-8') as file:
                        file.write(data2)
                        bot.send_message(call.message.chat.id, "❗️ ERROR HAS BEEN LOGGED")

                try:
                    os.remove(filenameaudio+'.mp3')
                except:
                    print("ERROR WHILE DELETING")
        threading.Thread(target=fnaudio).start()





# /SUBSCRIBE COMMAND
@bot.message_handler(commands=['subscribe'])
def subscribe_command(message):
    notSubscribed = True
    accessCode = message.text.replace('/subscribe', '')
    accessCode = accessCode.strip()
    if len(accessCode) == 0:
        bot.send_message(message.chat.id, "*Today's offer - ₹99* ([Pay here](https://paytm.me/C6C-akp))\n\n*Premium gang* - *USD 3$* ([Pay here](https://buymeacoffee.com/mortylabz/e/122212))\n\nSend the proof [here](https://t.me/ieatkidsforlunch) to get the access code.\n\nUse this Access code as\n'`/subscribe Youraccesscode`'\nto get Premium subscription\n\nSend '`/subscribe status`' to see your subscription status.\n\nYou will get:\n✅ - *Unlimited images*\n✅ - *Unlimited chat withAI*\n✅ - *No Rate limits for downloading*\n✅ - *Ultra realistic 4K images*\n✅ - *3X faster download speed*\n✅ - *Join our men's gang 🗿*\n✅ - *And many more*", parse_mode='Markdown', disable_web_page_preview=True)
    elif accessCode == 'status':
        res = isSubscriber(message.chat.id)
        if res == 1:
            bot.send_message(message.chat.id, "*STATUS : PREMIUM USER*\n\nYou have all the benefits granted!", parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, "*STATUS : FREE USER*\n\nSend `/subscribe` to see more details on how to become a *premium user*", parse_mode="Markdown")
    else:
        accessCode = accessCode.strip()
        userID = message.chat.id
        if subs_collection.find_one({"id":str(userID)}):
            notSubscribed = False
            bot.send_message(message.chat.id, "You are already subscribed to premium. Enjoy the benefits!")
        else:
            notSubscribed = True
        accepted = 0 # TRUE = 1 AND FALSE = 0
        if notSubscribed == True:
            tocheckcode = {'code':accessCode}
            if codes_collection.find_one(tocheckcode):
                accepted = 1
                subs_collection.insert_one({'id':str(userID)})
                bot.send_message(int(SUDO_ID), f"✅ @{str(message.from_user.username)} has subscribed to Morty AI\n\nID : {str(message.chat.id)}")
                bot.send_message(message.chat.id, "✅ Congrats!!\nYou are subscribed to get acccess to many features. Enjoy your benefits.")
            else:
                accepted = 0
        
        if accepted == 1:
            codes_collection.delete_one({"code":accessCode})
        if accepted == 0 and notSubscribed:
            bot.send_message(userID, "❗️ The Access code was incorrect.")





# /BC COMMAND (OWNER)
@bot.message_handler(commands=['bc'])
def bc_command(message):
    if str(message.chat.id) == SUDO_ID:
        query = message.text.replace('/bc', '')
        if len(query) == 0:
            bot.send_message(int(SUDO_ID), "Type something")
        else:
            bot.send_message(int(SUDO_ID), "Started delivering . . .")
            query = query.strip()
            for i in collection_users.find({}):
                try:
                    bot.send_message(int(i['id']), query, parse_mode='Markdown', disable_web_page_preview=True)
                    time.sleep(1)
                except:
                    print("User blocked")
                
            bot.send_message(int(SUDO_ID), "Message sent successfull!")
            






#/RESET COMMAND
@bot.message_handler(commands=['reset'])
def reset_data(message):
    if str(message.chat.id) == SUDO_ID:
        res = resetFile()
        if res == "200":
            bot.send_message(int(SUDO_ID), "users collection has been resetted!")



# /IMG COMMAND
@bot.message_handler(commands=['img'])
def img_command(message):
    query = message.text.replace('/img', '')
    if len(query) == 0:
        bot.send_message(message.chat.id, "Use in '`/img query`' format\nExample :\n\n`/img An astronaut in the ocean`", parse_mode='Markdown')
    else:
        
        userID = message.chat.id
        user = collection_users.find_one({"id":str(userID)})
        images_generated = user['images_generated']
        if images_generated >= 2 and isSubscriber(userID) == 0:
            bot.send_message(message.chat.id, "Your daily Limit has been reached!\nYou can get unlimited messages after subscription.")
            bot.send_message(message.chat.id, "Send `/subscribe` to see details on premium user.", parse_mode='Markdown')
        else:
            _message = bot.send_message(message.chat.id, "⌛️")
            bot.delete_message(message.chat.id, _message.message_id)
            response = generate_image(query, message)
            if response == 'err':
                bot.send_message(message.chat.id, "❗️ Some error occured")
            elif response == 'ratelimit':
                bot.send_message(message.chat.id, RATELIMIT)
            elif response == 'forbidden':
                bot.send_message(message.chat.id, FORBIDDEN)
            elif response == '500':
                bot.send_message(message.chat.id, ERROR500)
            else:
                bot.send_chat_action(chat_id=message.chat.id, action="upload_photo")
                response['created']
                images = response['images']
                try:
                    for image in images:
                        bot.send_photo(message.chat.id, image, caption="Generated by Morty AI")
                        images_generated = images_generated + 1
                        collection_users.update_one({"id":str(userID)}, {'$set':{"images_generated":images_generated}})
                except Exception as e:
                    print(e)
                    bot.send_message(message.chat.id, "❗️ Some error occured")




# /DEVELOPER COMMAND
@bot.message_handler(commands=['developer'])
def developer(message):
    keys = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Github", url="https://github.com/47hxl-53r"), InlineKeyboardButton("WhatsApp", url="https://wa.me/+918606672509"), InlineKeyboardButton("Telegram", url="https://t.me/ieatkidsforlunch"), InlineKeyboardButton("Buy me a coffee?", url="https://buymeacoffee.com/mortylabz"))
    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.chat.id, "This BOT is developed by Morty Labz", reply_markup=keys)




# /COUNT COMMAND
@bot.message_handler(commands=['count'])
def count_command(message):
    if str(message.chat.id) == SUDO_ID:
        resusers = collection_users.count_documents({})
        ressubs = subs_collection.count_documents({})
        resfree = resusers - ressubs
        bot.send_message(int(SUDO_ID), f"Total users : {resusers}\nFree users : {resfree}\nPremium users : {ressubs}")



# /ERRORS COMMAND (SUDO)
@bot.message_handler(commands=['errors'])
def errors_command(message):
    if str(message.chat.id) == SUDO_ID:
        errors = []
        with open('imgErrorLog.txt', 'r') as imgerrorfile:
            imgdata = imgerrorfile.read()
            if len(imgdata) == 0:
                errors.append("Image error logs are Empty!")
            else:
                errors.append(imgdata)
        with open('msgErrorLog.txt', 'r') as msgerrorfile:
            msgdata = msgerrorfile.read()
            if len(msgdata) == 0:
                errors.append("Message error logs are Empty!")
            else:
                errors.append(msgdata)

        with open('ytErrorLog.txt', 'r') as yterrorfile:
            ytdata = yterrorfile.read()
            if len(ytdata) == 0:
                errors.append("Youtube error logs are Empty!")
            else:
                errors.append(ytdata)

        for error in errors:
            bot.send_message(int(SUDO_ID), error, disable_web_page_preview=True)
        bot.send_message(int(SUDO_ID), "Send /clearerrors to clear error logs")

        


# /CLEARERRORS COMMAND
@bot.message_handler(commands=['clearerrors'])
def clearerrors_command(message):
    if str(message.chat.id) == SUDO_ID:
        with open('imgErrorLog.txt', 'w') as imgerrorfile:
            imgerrorfile.write("")
        with open('msgErrorLog.txt', 'w') as msgerrorfile:
            msgerrorfile.write("")
        with open('ytErrorLog.txt', 'w') as yterrorfile:
            yterrorfile.write("")
        bot.send_message(message.chat.id, "Error Logs cleared")




# /YOUTUBE COMMAND
@bot.message_handler(commands=['youtube'])
def youtube_command(message):
    query = message.text.replace('/youtube', '')
    if len(query) == 0:
        bot.send_message(message.chat.id, "Use in `/youtube url` format\nExample:\n\n`/youtube https://youtu.be/dQw4w9WgXcQ`", parse_mode="Markdown")
    else:
        bot.delete_message(message.chat.id, message.message_id)
        youtubevideourl = query.strip()
        if isValid(youtubevideourl):
            payload = youtubevideourl.replace('https://youtu.be/', '').strip()
            markup = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton("Video 📹", callback_data= f"video{payload}"), InlineKeyboardButton("Audio 🎧", callback_data=f"audiores{payload}"), InlineKeyboardButton("❌ Cancel ❌", callback_data="close"))
            bot.send_message(chat_id=message.chat.id,text=f"*URL : {youtubevideourl}*\n\n*Select an operation 👇*", reply_markup=markup, parse_mode="Markdown", disable_web_page_preview=True)
        else:
            bot.send_message(message.chat.id, "Invalid URL detected\n\nURL must start with `https://youtu.be/`", parse_mode="Markdown")





# /SCRAPE COMMAND
@bot.message_handler(commands=['scrape'])
def geturl(message):
    ok = message.text.replace('/scrape', '')
    if len(ok) == 0:
        bot.send_message(message.chat.id, "Send in `/scrape url` format (Including http:// or https://)\n\nExample:\n\n`/scrape https://google.com`", parse_mode="Markdown")
    else:
        url = ok.strip()
        if url.startswith('http://') or url.startswith('https://'):
            source_code = sourcecode(url)
            if source_code == 'err':
                bot.send_message(message.chat.id, "❗️ The given URL does not respond")
            elif source_code == 'timeout':
                bot.send_message(message.chat.id, '❗️ Timeout occured! Site responding too slow!')
            else:
                bot.send_chat_action(chat_id=message.chat.id, action="upload_document")
                end = randomNumber()
                filename = f'scraped-{end}.txt'
                try:
                    with open(filename, 'w+', encoding="utf-8") as f:
                        f.writelines(source_code)
                    file = open(filename, 'rb')
                    bot.send_document(message.chat.id, file)
                    file.close()
                except Exception as e7:
                    # PHASE 2 (EXCEPTION)
                    print(f"\n\n{e7.with_traceback}\n\n")
                    bot.send_message(message.chat.id, "❗️ Some error occured!")
                try:
                    # PHASE 3
                    os.remove(filename)
                except FileNotFoundError as fnf:
                    # PHASE 3 (EXCEPTION)
                    print(f"\n{fnf}\n")
        else:
            bot.send_message(message.chat.id, "❗️ Invalid URL detected")




# AI CHAT HANDLER (AI IS USED HERE)
@bot.message_handler(commands=['msg'])
def aiChatHandlerFunction(message):
    query = message.text.lower().replace('/msg', '').replace("sex", '').replace("fuck", '')
    if len(query) == 0:
        bot.send_message(message.chat.id, "Sent in '`/msg query`' format\nExample :\n\n`/msg How to make a pizza?`", parse_mode='Markdown')
    else:
        userId = message.chat.id
        user = collection_users.find_one({"id":str(userId)})
        messages_generated = user['messages_generated']
        if messages_generated >= 3 and isSubscriber(userId) == 0:
            bot.send_message(message.chat.id, "Your daily Limit has been reached!\nYou can get unlimited messages after subscription.")
            bot.send_message(message.chat.id, "Send `/subscribe` to see details on premium user.", parse_mode='Markdown')
        else:
            bot.send_chat_action(chat_id=message.chat.id, action="typing")
            query = query.strip()
            ai_response = askAI(query)
            if ai_response == 'ratelimit':
                bot.send_message(message.chat.id, RATELIMIT)
            elif ai_response == '500':
                bot.send_message(message.chat.id, ERROR500)
            elif ai_response == None:
                bot.send_message(message.chat.id, "❗️ Some error occured")
            else:
                bot.send_message(message.chat.id, ai_response)
                messages_generated = messages_generated + 1
                collection_users.update_one({"id":str(userId)}, {'$set':{"messages_generated":messages_generated}})

 


bot.infinity_polling()






