import openai, telebot, datetime, os, time, threading, re, requests
from yt_dlp import YoutubeDL
from youtube_search import YoutubeSearch
from telebot import types
from functions import askAI, resetFile, sourcecode, isValid, randomNumber, isSubscriber, json
from dotenv import load_dotenv, find_dotenv
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
telebot.apihelper.READ_TIMEOUT = 30
load_dotenv(find_dotenv())
TELE_API_KEY = os.getenv('TELE_API_KEY')
AI_API_KEY = os.getenv('AI_API_KEY')
SUDO_ID = os.getenv('SUDO_ID')

# INITIALISING THE BOT WITH TELEGRAM API
bot = telebot.TeleBot(TELE_API_KEY, threaded=True)
openai.api_key = AI_API_KEY


# FUNCTION TO SEARCH VIDEO AND RETURN DICTIONARY OF TITLE AND CORRESPONDING URL
def searchVideo(title):
    data = {}
    global resultsvid
    resultsvid = YoutubeSearch(title, max_results=10).to_dict()
    for i in resultsvid[0:]:
        data.update({f'{i["title"]}':f'{i["url_suffix"]}'})
    return data



def generate_image(prompt, message):
    num_image = 1
    output_format='url'
    size='1024x1024'
    invalid_words = ['doggy','mia khalifa','sunny leone','bathing','hot girl','inner','inner wear','sexy','boob', 'leah gotti','nipple','kiss','fuck', 'dick', 'sex','asshole', 'vagina', 'naked','penis', 'butt','breast', 'nude', 'titty', 'titties','poop']
    for i in invalid_words:
        if i.lower() in prompt:
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
    bot.send_message(message.chat.id, "Morty AI Bot is a chatbot that provides a range of AI-driven services to help people manage their day-to-day tasks. It can help you with tasks such as:\n\n🔰 *AI Image generation*\n🔰 *AI ChatBot*\n🔰 *Youtube video/audio downloading*\n🔰 *Music player*\n🔰 *Web scraping*\n🔰 *and more.*\n\nIt is powered by *natural language processing (NLP)* and *machine learning technology* to provide a personalized experience. To get started, simply send a message to Morty AI and it will respond with the help you need.\n\n*⚠️ BASIC COMMANDS ⚠️*\n/play - To play any music\n/img - To generate images based on your query\n/msg - Chat with Morty AI\n/youtube - Download YouTube video/audio\n/subscribe - Subscribe to premium\n/scrape - Web scraping\n/developer - Developer Information", parse_mode='Markdown')
    userID = message.chat.id
    exists = 1  # 0 is TRUE, 1 is FALSE
    with open('users.json','r') as file:
        json_data = json.load(file)
        for i in json_data:
            if i['id'] == str(userID):
                exists = 0
            elif i['id'] != str(userID):
                continue
    if exists == 1:
        towrite = {"id":str(userID), "images_generated":0}
        json_data.append(towrite)
        with open('users.json', 'w') as writefile:
            json.dump(json_data, writefile, indent=4)



@bot.message_handler(commands=['join'])
def join(message):
    markup = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Join support group", url="https://t.me/+_FoaeZ-tvIQ4OGE9"), InlineKeyboardButton("Join official channel", url="https://t.me/mortylab"))
    bot.send_message(message.chat.id, "Get support from here", reply_markup=markup)


# /PLAY COMMAND
@bot.message_handler(commands=['play'])
def play_command(message):
    id = message.chat.id
    query = message.text.replace('/play','')
    if len(query) == 0:
        bot.send_message(id, "Use `/play songname` format", parse_mode="Markdown")
    else:
        if 'movie' in query.lower() or 'cinema' in query.lower() or 'film' in query.lower() or 'full movie' in query.lower() or '2023' in query.lower():
            bot.send_message(message.chat.id, "Movies are not allowed!")
        else:
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
                InlineKeyboardButton("❌ Cancel ❌", callback_data="cancel")
            )
            global filename
            filename = f'{query.replace(" ", "")}.mp3'
            bot.edit_message_text(message_id=message_id,chat_id=chat_id, text=f"Found {str(len(dictdata))} results for {query} 🔎\n\n👇", reply_markup=first_markup)
        



# CALLBACK QUERY HANDLERS FOR ALL COMMANDS WITH INLINEKEYBOARD CALLBACKS
@bot.callback_query_handler(func=lambda message: True)
def callback_query_handler(call):
    if call.data.startswith('hehe'):
        playurl = 'https://youtube.com'+call.data.replace('hehe','')
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        _message = bot.send_message(chat_id=call.message.chat.id, text="_Fetching music in best quality as possible . . ._", parse_mode="Markdown")
        html = requests.get(playurl).text
        titleplay = re.findall(r"<title>(.*?)</title>", html)[0]
        authorplay = re.findall(r"\"author\":\"(.*?)\"", html)[0]
        viewsplay = re.findall(r"\"viewCountText\":{\"simpleText\":\"(.*?)\"", html)[0]
        published_onplay = re.findall(r"\"dateText\":{\"simpleText\":\"(.*?)\"", html)[0]
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
            try:
                def download():
                    ydl.download(playurl)
                downloadhehe = threading.Thread(target=download)
                downloadhehe.run()
            except Exception as e:
                bot.edit_message_text(chat_id=_message.chat.id, message_id=_message.message_id, text="`❗️ Exception occured`", parse_mode="Markdown")
                data = f'ERROR WHILE DOWNLOADING URL\n\nURL : {playurl}\n{e}\nTRACEBACK\n\n{e.with_traceback}\n\n---------------------\n\n'
                with open('ytErrorLog.txt', 'a', encoding='utf-8') as file:
                    file.write(data)
                    bot.send_message(call.message.chat.id, "❗️ ERROR HAS BEEN LOGGED")
                

        # PHASE 2
        try:
            if os.path.getsize(filename+'.mp3') >= 50000000:
                bot.send_message(call.message.chat.id, "The filesize is too large! Subscribe to premium to get rid of restrictions!")
                bot.delete_message(chat_id=_message.chat.id, message_id=_message.message_id)
            else:
                markupclose = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("❌ Close player ❌", callback_data="closeplayer"))
                caption = f'{titleplay} | {authorplay}\n\n*Views* : {viewsplay}\n*Author* : {authorplay}\n*Published on* : {published_onplay}\n\n\n[Morty AI](https://t.me/morty_ai_bot)'
                with open(filename+'.mp3', 'rb') as audiofile:
                    bot.send_audio(chat_id=call.message.chat.id,audio=audiofile, performer=authorplay, title=titleplay, caption=caption, parse_mode='Markdown', reply_markup=markupclose)
                    bot.delete_message(chat_id=_message.chat.id, message_id=_message.message_id)
                
        except Exception as n:
            bot.edit_message_text(chat_id=_message.chat.id, message_id=_message.message_id, text="❗️ ERROR WHILE SENTING")
            data2 = f'ERROR WHILE SENTING IN /PLAY\n\nURL : {playurl}\n{n}\nTRACEBACK\n\n{n.with_traceback}\n\n---------------------\n\n'
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
    

    elif call.data == 'feedback':
        newwmarkup = InlineKeyboardMarkup(row_width=1)
        newwmarkup.add(
            InlineKeyboardButton("Click here", url='https://t.me/dailychannelsbot?start=morty_ai_bot'),
            InlineKeyboardButton("Close", callback_data="close"))
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=newwmarkup)

    elif call.data == 'close':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    elif call.data == 'closeplayer':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    elif call.data == 'cancel':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    elif call.data == 'dwvideo':
        markup = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("High Resolution", callback_data="highresolution"), InlineKeyboardButton("Low resolution", callback_data="lowresolution"))
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)
    
    elif call.data == 'highresolution':
        global filenamevideo
        filenamevideo = f'video{str(randomNumber())}.ogg'
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="⌛️")
        ydl_optsvideo = {
            "format":"bestvideo[ext=ogg]+bestaudio[ext=mp3]/best",
            "outtmpl":filenamevideo,
            "quiet":True,
        }
        with YoutubeDL(ydl_optsvideo) as ydl:
            try:
                def downloadvideo():
                    ydl.download(youtubevideourl)
                videothread = threading.Thread(target=downloadvideo)
                videothread.run()
            except Exception as e:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="`❗️ Exception occured`", parse_mode="Markdown")
                data = f'ERROR WHILE DOWNLOADING VIDEO\n\nURL : {youtubevideourl}\n{e}\nTRACEBACK\n\n{e.with_traceback}\n\n---------------------\n\n'
                with open('ytErrorLog.txt', 'a', encoding='utf-8') as file:
                    file.write(data)
                    bot.send_message(call.message.chat.id, "❗️ ERROR HAS BEEN LOGGED")
            try:
                if os.path.getsize(filenamevideo) >= 50000000:
                     bot.send_message(call.message.chat.id, "Filesize is too large! Subscribe to premium to remove restrictions!")
                     bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                else:
                    html = requests.get(youtubevideourl).text
                    title = re.findall(r"<title>(.*?) - YouTube</title>", html)[0]
                    with open(filenamevideo, 'rb') as videofile:
                        def sendvideo():
                            bot.send_video(chat_id=call.message.chat.id, video=videofile, caption=f"{title}\n\n[Morty AI](https://t.me/morty_ai_bot)", parse_mode="Markdown")
                        sendhehee = threading.Thread(target=sendvideo)
                        sendhehee.run()
                        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            
            except Exception as q:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="❗️ ERROR WHILE SENTING")
                data3 = f'ERROR WHILE SENTING VIDEO\n\nURL : {youtubevideourl}\n{q}\nTRACEBACK\n\n{q.with_traceback}\n\n---------------------\n\n'
                with open('ytErrorLog.txt', 'a', encoding='utf-8') as file:
                    file.write(data3)
                    bot.send_message(call.message.chat.id, "❗️ ERROR HAS BEEN LOGGED")

            try:
                os.remove(filenamevideo)
            except:
                print("ERROR WHILE DELETING")


    elif call.data == 'lowresolution':
        global filenamevideolow
        filenamevideolow = f'videolow{str(randomNumber())}.mp4'
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="⌛️")
        ydl_optsvideolow = {
            "format":"worstvideo[ext=ogg]+worstaudio/worst",
            "outtmpl":filenamevideolow,
            "quiet":True,
        }
        with YoutubeDL(ydl_optsvideolow) as ydl:
            try:
                def downloadvideolow():
                    ydl.download(youtubevideourl)
                videothread1 = threading.Thread(target=downloadvideolow)
                videothread1.run()
            except Exception as e:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="`❗️ Exception occured`", parse_mode="Markdown")
                data5 = f'ERROR WHILE DOWNLOADING LOW VIDEO URL\n\nURL : {youtubevideourl}\n{e}\nTRACEBACK\n\n{e.with_traceback}\n\n---------------------\n\n'
                with open('ytErrorLog.txt', 'a', encoding='utf-8') as file:
                    file.write(data5)
                    bot.send_message(call.message.chat.id, "❗️ ERROR HAS BEEN LOGGED")  
            try:
                if os.path.getsize(filenamevideolow) >= 50000000:
                    bot.send_message(call.message.chat.id, "The filesize is too large! Subscribe to premium to get of restrictions!")
                else:
                    html = requests.get(youtubevideourl).text
                    title = re.findall(r"<title>(.*?) - YouTube</title>", html)[0]
                    with open(filenamevideolow, 'rb') as videofile:
                        def sendvideolow():
                            bot.send_video(chat_id=call.message.chat.id,video=videofile,  caption=f"{title}")
                        sendhehee1 = threading.Thread(target=sendvideolow)
                        sendhehee1.run()
                        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            
            except Exception as q:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="❗️ ERROR WHILE SENTING")
                data6 = f'ERROR WHILE SENTING LOW VIDEO\n\nURL : {youtubevideourl}\n{q}\nTRACEBACK\n\n{q.with_traceback}\n\n---------------------\n\n'
                with open('ytErrorLog.txt', 'a', encoding='utf-8') as file:
                    file.write(data6)
                    bot.send_message(call.message.chat.id, "❗️ ERROR HAS BEEN LOGGED")

            try:
                os.remove(filenamevideolow)
            except:
                print("ERROR WHILE DELETING")
    elif call.data == 'dwaudio':
        html2 = requests.get(youtubevideourl).text
        titleaudio = re.findall(r"<title>(.*?)</title>", html2)[0]
        filenameaudio = titleaudio.replace('|', '')
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="_Downloading audio in best quality as possible . . ._",parse_mode='Markdown')
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
            try:
                def downloadaudio():
                    ydl.download(youtubevideourl)
                downloadheheaudio = threading.Thread(target=downloadaudio)
                downloadheheaudio.run()
            except Exception as e:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="`❗️ Exception occured`", parse_mode="Markdown")
                data = f'ERROR WHILE DOWNLOADING AUDIO\n\nURL : {youtubevideourl}\n{e}\nTRACEBACK\n\n{e.with_traceback}\n\n---------------------\n\n'
                with open('ytErrorLog.txt', 'a', encoding='utf-8') as file:
                    file.write(data)
                    bot.send_message(call.message.chat.id, "❗️ ERROR HAS BEEN LOGGED")

            try:
                caption = f'{titleaudio}\n\nDownloaded by [Morty AI](https://t.me/morty_ai_bot)'
                with open(filenameaudio+'.mp3', 'rb') as audiofile:
                    def sendaudio():
                        bot.send_audio(chat_id=call.message.chat.id,audio=audiofile, caption=caption, parse_mode='Markdown')
                    sendheheaudio = threading.Thread(target=sendaudio)
                    sendheheaudio.run()
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



# /SUBSCRIBE COMMAND
@bot.message_handler(commands=['subscribe'])
def subscribe_command(message):
    notSubscribed = True
    accessCode = message.text.replace('/subscribe', '')
    accessCode = accessCode.strip()
    if len(accessCode) == 0:
        bot.send_message(message.chat.id, "Here is the [link](https://paytm.me/FYCO-4w) for payment\n\nPay just *INR 99/-* and send the proof [here](https://t.me/ieatkidsforlunch) to get the access code.\n\nUse this Access code as\n'`/subscribe Youraccesscode`'\nto get Premium subscription\n\nSend '`/subscribe status`' to see your subscription status.\n\nYou will get:\n✅ - *Unlimited images*\n✅ - *Ultra realistic 4K images*\n✅ - *Accurate image rendering*\n✅ - *And many more...*", parse_mode='Markdown', disable_web_page_preview=True)
    elif accessCode == 'status':
        res = isSubscriber(message.chat.id)
        if res == 1:
            bot.send_message(message.chat.id, "*STATUS : PREMIUM USER*\n\nYou have all the benefits granted!", parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, "*STATUS : FREE USER*\n\nSend `/subscribe` to see more details on how to become a *premium user*", parse_mode="Markdown")
    else:
        accessCode = accessCode.strip()
        userID = message.chat.id
        with open('subscribers.json', 'r') as file:
            json_data = json.load(file)
            for i in json_data:
                if i['id'] == str(userID):
                    bot.reply_to(message, "You are already a subscriber, enjoy the benefits")
                    notSubscribed = False
                else:
                    notSubscribed = True
        accepted = 1 # TRUE = 0 AND FALSE = 1
        if notSubscribed:
            with open('Accesscodes.json', 'r') as file:
                json_code_data = json.load(file)
                for i in json_code_data:
                    if i['code'] == accessCode:
                        accepted = 0
                        bot.send_message(int(SUDO_ID), f"✅ @{str(message.from_user.username)} has subscribed to Morty AI\n\nID : {str(message.chat.id)}")
                        bot.send_message(message.chat.id, "✅ Congrats!!\nYou are subscribed to get acccess to many features. Enjoy your benefits.")
                        break
                    else:
                        accepted = 1
        if accepted == 0:
            for i in json_code_data:
                if i['code'] == accessCode:
                    json_code_data.remove(i)
            with open('Accesscodes.json', 'w') as filetowrite:
                json.dump(json_code_data, filetowrite, indent=4)
            towrite = {"id": str(userID)}
            json_data.append(towrite)
            with open('subscribers.json', 'w') as file:
                json.dump(json_data, file, indent=4)
        if accepted == 1 and notSubscribed == True:
            bot.send_message(userID, "❗️ The Access code was incorrect.")



# /BC COMMAND (OWNER)
@bot.message_handler(commands=['bc'])
def bc_command(message):
    if str(message.chat.id) == SUDO_ID:
        query = message.text.replace('/bc', '')
        if len(query) == 0:
            bot.send_message(int(SUDO_ID), "Type something")
        else:
            with open('users.json', 'r') as users:
                json_data = json.loads(users.read())

            bot.send_message(int(SUDO_ID), "Started delivering . . .")
            for i in json_data:
                bot.send_message(int(i['id']), query, parse_mode='Markdown', disable_web_page_preview=True)
                time.sleep(5)

            bot.send_message(int(SUDO_ID), f"Message sent!\n\nMessage : {query}")



# /DATA
@bot.message_handler(commands=['data'])
def data_command(message):
    if str(message.chat.id) == SUDO_ID:
        with open('users.json','r') as users:
            bot.send_document(chat_id=message.chat.id, document=users)
        with open('subscribers.json','r') as subscribers:
            bot.send_document(chat_id=message.chat.id, document=subscribers)
        with open('Accesscodes.json','r') as codes:
            bot.send_document(chat_id=message.chat.id, document=codes)



# /RESET COMMAND
@bot.message_handler(commands=['reset'])
def reset_data(message):
    if str(message.chat.id) == SUDO_ID:
        res = resetFile()
        if res == "200":
            bot.send_message(message.chat.id, "users.json has been resetted!")




# /IMG COMMAND
@bot.message_handler(commands=['img'])
def img_command(message):
    query = message.text.replace('/img', '')
    if len(query) == 0:
        bot.send_message(message.chat.id, "Sent in '`/img query`' format\nExample :\n\n`/img An astronaut in the ocean`", parse_mode='Markdown')
    else:
        userID = message.chat.id
        images_generated = 0
        with open('users.json','r') as file:
            json_data = json.loads(file.read())
            for i in json_data:
                if i['id'] == str(userID):
                    images_generated = i['images_generated']
                    if images_generated >= 3 and isSubscriber(userID) == 0:
                        bot.send_message(message.chat.id, "Your daily Limit has been reached!\nYou can get unlimited images after subscription.")
                        bot.send_message(message.chat.id, "Send `/subscribe` to see details on premium user", parse_mode='Markdown')
                    else:
                        response = generate_image(query, message)
                        if response == 'err':
                            bot.send_message(message.chat.id, "❗️ Some error occured")
                        else:
                            response['created']
                            images = response['images']
                            try:
                                for image in images:
                                    bot.send_photo(message.chat.id, image, caption="Generated by Morty AI.")
                                    images_generated = images_generated + 1
                                    i['images_generated'] = images_generated
                            except Exception as e:
                                print(e)
                                bot.send_message(message.chat.id, "❗️ Some error occured")
        with open('users.json', 'w') as writefile:
            json.dump(json_data, writefile, indent=4)




# /DEVELOPER COMMAND
@bot.message_handler(commands=['developer'])
def developer(message):
    keys = InlineKeyboardMarkup(row_width=1)
    gh = types.InlineKeyboardButton(text="Github", url="https://github.com/47hxl-53r")
    wp = types.InlineKeyboardButton(text="WhatsApp", url="https://wa.me/+918606672509")
    tg = types.InlineKeyboardButton(text="Telegram", url="https://t.me/ieatkidsforlunch")
    bm = types.InlineKeyboardButton(text="Buy me a coffee?", url="https://buymeacoffee.com/mortylabz")
    keys.add(gh, wp, tg)
    bot.send_message(message.chat.id, "This BOT is developed by Morty Labz", reply_markup=keys)




# /COUNT COMMAND
@bot.message_handler(commands=['count'])
def count_command(message):
    userID = message.chat.id
    if str(userID) == SUDO_ID:
        with open('users.json', 'r') as usersfile:
            json_data = json.load(usersfile)
            users = []
            for i in json_data:
                users.append(i['id'])
        with open('subscribers.json', 'r') as subsfile:
            json_subs_data = json.load(subsfile)
            premium_users = []
            for j in json_subs_data:
                premium_users.append(j['id'])
        users_count = len(users)
        premium_count = len(premium_users)
        now = datetime.datetime.now()
        bot.send_message(int(SUDO_ID), f"Total Users : {str(users_count)}\n\nFree users : {str(users_count - premium_count)}\nPremium users : {str(premium_count)}\nTime : {str(now)}")




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
        global youtubevideourl
        youtubevideourl = query.strip()
        if isValid(youtubevideourl):
            markup = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Download Video 📹", callback_data="dwvideo"), InlineKeyboardButton("Download Audio 🎧", callback_data="dwaudio"))
            bot.send_message(message.chat.id, "Select an operation 👇", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "Invalid URL detected")




# /SCRAPE COMMAND
@bot.message_handler(commands=['scrape'])
def geturl(message):
    global rescrape
    ok = message.text.replace('/scrape', '')
    if len(ok == 0):
        bot.send_message(message.chat.id, "Send in `/scrape url` format (Including http:// or https://)\nExample:\n`/scrape https://google.com`", parse_mode="Markdown")
    else:
        url = ok.strip()
        if url.startswith('http://') or url.startswith('https://'):
            source_code = sourcecode(url)
            if source_code == 'err':
                bot.send_message(message.chat.id, "❗️ The given URL does not respond")
            elif source_code == 'timeout':
                bot.send_message(message.chat.id, '❗️ Timeout occured! Site responding too slow!')
            else:
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
    query = message.text.replace('/msg', '')
    if len(query) == 0:
        bot.send_message(message.chat.id, "Sent in '`/msg query`' format\nExample :\n\n`/msg How to make a pizza?`", parse_mode='Markdown')
    else:
        query = query.strip()
        ai_response = askAI(query)
        if ai_response == None:
            bot.send_message(message.chat.id, "❗️ Some error occured")
        else:
            bot.send_message(message.chat.id, ai_response)




bot.infinity_polling()






