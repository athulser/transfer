import openai, telebot, datetime, os, time, re, requests, threading
from yt_dlp import YoutubeDL
from telebot import custom_filters
from pymongo import MongoClient
from youtube_search import YoutubeSearch
from functions import resetFile, sourcecode, isValid, randomNumber, isSubscriber, FORBIDDEN, ERROR500, RATELIMIT
from dotenv import load_dotenv, find_dotenv
# from openai.error import RateLimitError, InvalidRequestError, APIError
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
telebot.apihelper.READ_TIMEOUT = 60
load_dotenv(find_dotenv())
STABLEAPIKEY = os.getenv("STABLEAPIKEY")
TELE_API_KEY = os.getenv('TELE_API_KEY')
AI_API_KEY = os.getenv('AI_API_KEY')
SUDO_ID = os.getenv('SUDO_ID')


cluster = MongoClient("mongodb+srv://tzvri75136:Atulrv2005@mortydb.t0mwlvs.mongodb.net/?retryWrites=true&w=majority")
db = cluster['mortydb']
collection_users = db['users']
subs_collection = db['subscribers']
codes_collection = db['Accesscodes'] 
redeem_collection = db['redeemcodes']
groups_collection = db['groups']


# INITIALISING THE BOT WITH TELEGRAM API
bot = telebot.TeleBot(TELE_API_KEY, threaded=True)
openai.api_key = AI_API_KEY
active_users = {}
play_active_users = {}



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
    # num_image = 1
    # output_format='url'
    # size='1024x1024'
    invalid_words = ['nood','without clothes','girl without','bare body','stab','cum','aunty','girlfriend','sister','handjob','licking','milf','hentai','donald','trump','sex','seduc','dwayne','clevage','girl wearing','fuk','pussy','horny','no clothes','suck','copulation','twerking','scarlett','fck','narendra','gangbang','intercourse','stepmom','stepsister','xxx','xnxx','whore','ass','hot girl','underwear','girl bathing','xi jingping','modi','brazzers','biden','joe','salman','porn','doggy','mia khalifa','sunny leone','bathing','hot girl','inner','inner wear','nanked','sexy','boob', 'leah gotti','nipple','kiss','fuck', 'dick', 'sex','asshole', 'vagina', 'naked','penis', 'butt','breast','chest','naced','abdomen','making out','tits','flirting','firting', 'nude', 'titty', 'titties','poop']
    for i in invalid_words:
        if i in prompt.lower():
            bot.send_message(message.chat.id, "Your query contains forbidden words")
            return 'err'
    try:
        import requests
        
        URL = 'https://stablediffusionapi.com/api/v3/text2img'
        response = requests.post(URL, json={"key":STABLEAPIKEY, "prompt":prompt, "width":"512", "height":"512", "samples":"1", "enhance_prompt":"yes"})
        res = response.json()
        print(res)
        return res['output'][0]

    except Exception as e:
        with open('imgErrorLog.txt', 'a') as file:
            data = f'QUERY : {prompt}\n\n{e}---------------------\n\n'
            file.write(data)
            print("ERROR HAS BEEN LOGGED TO FILE")
            bot.send_message(message.chat.id, e)
            return 'err'
    #     images = []
    #     response = openai.Image.create(
    #         prompt=prompt,
    #         n=num_image,
    #         size=size,
    #         response_format=output_format
    #     )
    #     if output_format == 'url':
    #         for image in response['data']:
    #             images.append(image.url)
    #     elif output_format == 'b64_json':
    #         images.append(image.b64_json)
    #     return {'created':datetime.datetime.fromtimestamp(response['created']), 'images':images}
    # except RateLimitError:
    #     return 'ratelimit'
    # except InvalidRequestError:
    #     return 'forbidden'
    # except APIError:
    #     return '500'
    # except Exception as e:
    #     with open('imgErrorLog.txt', 'a') as file:
    #         data = f'QUERY : {prompt}\n\n{e}---------------------\n\n'
    #         file.write(data)
    #         print("ERROR HAS BEEN LOGGED TO FILE")
    #         bot.send_message(message.chat.id, e)
    #         return 'err'



@bot.my_chat_member_handler()
def me(message: telebot.types.ChatMemberUpdated):
    new = message.new_chat_member
    if new.status == 'member':
        bot.send_message(message.chat.id, "King is here!! HHAHAHAHA!!\n\nGive me access to messages and I can start doing my job :)")
        groups_collection.insert_one({"id":str(message.chat.id)})

@bot.message_handler(commands=['start'], chat_types=['private'])
def start_message(message):
    userID = message.chat.id
    usermsg = message.message_id
    bot.delete_message(chat_id=userID, message_id=usermsg)
    bot.send_message(userID, "ᴍᴏʀᴛʏ ᴀɪ ʙᴏᴛ ɪꜱ ᴀ ᴄʜᴀᴛʙᴏᴛ ᴛʜᴀᴛ ᴘʀᴏᴠɪᴅᴇꜱ ᴀ ʀᴀɴɢᴇ ᴏꜰ ᴀɪ-ᴅʀɪᴠᴇɴ ꜱᴇʀᴠɪᴄᴇꜱ ᴛᴏ ʜᴇʟᴘ ᴘᴇᴏᴘʟᴇ ᴍᴀɴᴀɢᴇ ᴛʜᴇɪʀ ᴅᴀʏ-ᴛᴏ-ᴅᴀʏ ᴛᴀꜱᴋꜱ. It can help you with tasks such as:\n\n🔰 *ʏᴏᴜᴛᴜʙᴇ ᴠɪᴅᴇᴏ/ᴀᴜᴅɪᴏ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ*\n🔰 *ᴍᴜꜱɪᴄ ᴘʟᴀʏᴇʀ*\n🔰 *ᴡᴇʙ ꜱᴄʀᴀᴘɪɴɢ*\n🔰 *ᴀɴᴅ ᴍᴏʀᴇ.*\n\n*ɪᴛ ɪꜱ ᴘᴏᴡᴇʀᴇᴅ ʙʏ ɴᴀᴛᴜʀᴀʟ ʟᴀɴɢᴜᴀɢᴇ ᴘʀᴏᴄᴇꜱꜱɪɴɢ (ɴʟᴘ)* ᴀɴᴅ *ᴍᴀᴄʜɪɴᴇ ʟᴇᴀʀɴɪɴɢ ᴛᴇᴄʜɴᴏʟᴏɢʏ* ᴛᴏ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴘᴇʀꜱᴏɴᴀʟɪᴢᴇᴅ ᴇxᴘᴇʀɪᴇɴᴄᴇ. ᴛᴏ ɢᴇᴛ ꜱᴛᴀʀᴛᴇᴅ, ꜱɪᴍᴘʟʏ ꜱᴇɴᴅ ᴀ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ᴍᴏʀᴛʏ ᴀɪ ᴀɴᴅ ɪᴛ ᴡɪʟʟ ʀᴇꜱᴘᴏɴᴅ ᴡɪᴛʜ ᴛʜᴇ ʜᴇʟᴘ ʏᴏᴜ ɴᴇᴇᴅ.\n\n*⚠️ BASIC COMMANDS ⚠️*\n/img - ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ ɪᴍᴀɢᴇ\n/play - ᴛᴏ ᴘʟᴀʏ ᴀɴʏ ᴍᴜꜱɪᴄ\n/youtube - ᴅᴏᴡɴʟᴏᴀᴅ ʏᴏᴜᴛᴜʙᴇ ᴠɪᴅᴇᴏ/ᴀᴜᴅɪᴏ\n/subscribe - ꜱᴜʙꜱᴄʀɪʙᴇ ᴛᴏ ᴘʀᴇᴍɪᴜᴍ\n/scrape - ᴡᴇʙ ꜱᴄʀᴀᴘɪɴɢ\n/join - ᴊᴏɪɴ ᴏᴜʀ ʙᴀꜱᴇᴍᴇɴᴛꜱ\n/developer - ᴅᴇᴠᴇʟᴏᴘᴇʀ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ", parse_mode='Markdown', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("❌ ᴄʟᴏꜱᴇ ❌", callback_data='close')))
    res = collection_users.find_one({"id":str(userID)})
    if not res:
        towrite = {'id':str(userID), "credits":2, "joinedOn":datetime.datetime.now().timestamp()}
        collection_users.insert_one(towrite)


    
@bot.message_handler(['data'], chat_types=['private'])
def data(message):
    if str(message.chat.id) == SUDO_ID:
        for i in codes_collection.find({}):
            bot.send_message(int(SUDO_ID), 'subscription code : '+i['code'])
        for p in redeem_collection.find({}):
            bot.send_message(int(SUDO_ID), f"Code : {p['code']}\nCredits : {p['credits']}")
    



@bot.message_handler(commands=['join'], chat_types=['private'])
def join(message):
    markupjoin = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("ᴊᴏɪɴ ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ", url="https://t.me/+_FoaeZ-tvIQ4OGE9"), InlineKeyboardButton("ᴊᴏɪɴ ᴏꜰꜰɪᴄɪᴀʟ ᴄʜᴀɴɴᴇʟ", url="https://t.me/mortylab"), InlineKeyboardButton("🗿 ᴊᴏɪɴ ᴍᴇɴ'ꜱ ɢᴀɴɢ 🗿", callback_data="checkpremium"))
    bot.send_message(message.chat.id, "Get support from here", reply_markup=markupjoin)


@bot.message_handler(commands=['play'], chat_types=['group', 'supergroup'])
def no(message):
    bot.reply_to(message=message, text="ꜱᴇɴᴅ ɪɴ '.ᴘʟᴀʏ ꜱᴏɴɢɴᴀᴍᴇ' ꜰᴏʀᴍᴀᴛ\nExample:\n\n`.play butterfly effect`")



# /PLAY COMMAND
@bot.message_handler(commands=['play'], chat_types=['private'])
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





@bot.message_handler(content_types=['text'], chat_types=['group', 'supergroup'], text_startswith=('.play', '.Play'))
def playgroup(message):
    query = message.text.lower().replace('.play', '').strip()
    if len(query) == 0:
        bot.send_message(message.chat.id, "Use in `.play songname` format\nExample:\n\n`.play intentions`", parse_mode="Markdown")
    else:
        if 'movie' in query.lower() or 'cinema' in query.lower() or 'film' in query.lower() or 'full movie' in query.lower() or '2023' in query.lower():
            bot.send_message(message.chat.id, "Stop trying to download movies bro...", parse_mode="Markdown")
        else:
            bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            _message = bot.send_message(message.chat.id, "⌛️", parse_mode='Markdown')
            chat_id, message_id = _message.chat.id, _message.message_id
            dictdataa = searchVideo(query)
            first_markup = InlineKeyboardMarkup()
            for title, urlsuffix in dictdataa.items():
                urlwithdudu = 'fuc'+ urlsuffix
                first_markup.add(
                    InlineKeyboardButton(title, callback_data=urlwithdudu)
                )
            first_markup.add(
                InlineKeyboardButton("❌ Cancel ❌", callback_data="close")
            )
            bot.edit_message_text(message_id=message_id,chat_id=chat_id, text=f"*Found {len(dictdataa)} results for {query} 🔎*\n\n👇", reply_markup=first_markup, parse_mode="Markdown")




# CALLBACK QUERY HANDLERS FOR ALL COMMANDS WITH INLINEKEYBOARD CALLBACKS
@bot.callback_query_handler(func=lambda message: True)
def callback_query_handler(call):
    if call.data.startswith('fuc'):
        now = datetime.datetime.now().timestamp()
        if call.message.from_user.id in active_users:
            if time_difference(active_users[call.message.from_user.id]):
                active_users[call.message.from_user.id] = now
            else:
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                bot.send_message(chat_id=call.message.chat.id,disable_web_page_preview=True, parse_mode="Markdown", text="*ᴅᴏᴡɴʟᴏᴀᴅꜱ ᴀʀᴇ ʟɪᴍɪᴛᴇᴅ ᴛᴏ 1 ᴅᴏᴡɴʟᴏᴀᴅ ᴘᴇʀ 60 ꜱᴇᴄᴏɴᴅꜱ* (%dꜱ ʀᴇᴍᴀɪɴɪɴɢ)\n\n[Morty AI](https://t.me/morty_ai_bot)"%(60-(now - active_users[call.message.from_user.id])))
                return
        else:
            active_users[call.message.from_user.id] = now
        
        def playsong():
            groupplayurl = 'https://youtu.be'+call.data.replace('fuc','').strip()
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            _message = bot.send_message(chat_id=call.message.chat.id, text="𝚂𝚃𝙰𝚃𝚄𝚂 : 𝙵𝚎𝚝𝚌𝚑𝚒𝚗𝚐 𝚜𝚝𝚛𝚎𝚊𝚖𝚜")
            html = requests.get(groupplayurl).text
            titleplay = re.findall(r"<title>(.*?)</title>", html)[0]
            authorplay = re.findall(r"\"author\":\"(.*?)\"", html)[0]
            viewsplay = re.findall(r"\"viewCountText\":{\"simpleText\":\"(.*?)\"", html)[0]
            published_onplay = re.findall(r"\"dateText\":{\"simpleText\":\"(.*?)\"", html)[0]
            filename = f'groupplay-{str(randomNumber())}'
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
                bot.edit_message_text(chat_id=_message.chat.id, message_id=_message.message_id, text="𝚂𝚃𝙰𝚃𝚄𝚂 : 𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍 𝚒𝚗 𝚙𝚛𝚘𝚐𝚛𝚎𝚜𝚜")
                try:
                    ydl.download(groupplayurl)
                    bot.edit_message_text(chat_id=_message.chat.id, message_id=_message.message_id, text="𝚂𝚃𝙰𝚃𝚄𝚂 : 𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍 𝚌𝚘𝚖𝚙𝚕𝚎𝚝𝚎")
                except Exception as e:
                    bot.edit_message_text(chat_id=_message.chat.id, message_id=_message.message_id, text="`❗️ Exception occured`", parse_mode="Markdown")
                    data = f'ERROR WHILE DOWNLOADING URL GROUP PLAY\n\nURL : {groupplayurl}\n{e}---------------------\n\n'
                    with open('ytErrorLog.txt', 'a', encoding='utf-8') as file:
                        file.write(data)
                        bot.send_message(call.message.chat.id, "❗️ ERROR HAS BEEN LOGGED")
                
                try:
                    bot.send_chat_action(chat_id=call.message.chat.id, action="upload_audio")
                    bot.edit_message_text(chat_id=_message.chat.id, message_id=_message.message_id, text='⌛️')
                    if os.path.getsize(filename+'.mp3') >= 50000000:
                        bot.send_message(chat_id=call.message.chat.id, text="The filesize is too large!")
                        bot.delete_message(chat_id=_message.chat.id, message_id=_message.message_id)
                    else:
                        markupclose = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("❌ ᴄʟᴏꜱᴇ ᴘʟᴀʏᴇʀ ❌", callback_data="close"))
                        caption = f'{titleplay} | {authorplay}\n\n*Views* : {viewsplay}\n*Author* : {authorplay}\n*Published on* : {published_onplay}\n\n\n[Join MortyLabz](https://t.me/mortylab) | [Donate me](https://buymeacoffee.com/mortylabz)'
                        with open(filename+'.mp3', 'rb') as audiofile:
                            bot.send_audio(chat_id=call.message.chat.id,audio=audiofile, performer=authorplay, title=titleplay, caption=caption, parse_mode='Markdown', reply_markup=markupclose)
                            bot.delete_message(chat_id=_message.chat.id, message_id=_message.message_id)

                except Exception as n:
                    bot.edit_message_text(chat_id=_message.chat.id, message_id=_message.message_id, text="❗️ ERROR WHILE SENTING")
                    data2 = f'ERROR WHILE SENTING IN GROUP /PLAY\n\nURL : {groupplayurl}\n{n}\n\n---------------------\n\n'
                    with open('ytErrorLog.txt', 'a', encoding='utf-8') as file:
                        file.write(data2)
                        bot.send_message(call.message.chat.id, "❗️ ERROR HAS BEEN LOGGED")
                
                try:
                    os.remove(filename+'.mp3')
                except:
                    print("ERROR WHILE DELETING")
                newmarkup = InlineKeyboardMarkup(row_width=1)
                newmarkup.add(
                    InlineKeyboardButton("ꜰᴇᴇᴅʙᴀᴄᴋ", callback_data='feedback'),
                    InlineKeyboardButton("ᴄʟᴏꜱᴇ", callback_data="close"))
                bot.send_message(call.message.chat.id, "_Mind giving me a feedback?_", parse_mode="Markdown", reply_markup=newmarkup)
        
        threading.Thread(target=playsong).start()




    elif call.data.startswith('hehe'):
        if isSubscriber(call.message.chat.id) == 0:
            now = datetime.datetime.now().timestamp()
            if call.message.chat.id in active_users:
                if time_difference(active_users[call.message.chat.id]):
                    active_users[call.message.chat.id] = now
                else:
                    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                    bot.send_message(chat_id=call.message.chat.id, parse_mode="Markdown", text="*ᴅᴏᴡɴʟᴏᴀᴅꜱ ᴀʀᴇ ʟɪᴍɪᴛᴇᴅ ᴛᴏ 1 ᴅᴏᴡɴʟᴏᴀᴅ ᴘᴇʀ 60 ꜱᴇᴄᴏɴᴅꜱ* (%dꜱ ʀᴇᴍᴀɪɴɪɴɢ)\n\n/subscribe ᴛᴏ ɢᴇᴛ ʀɪᴅ ᴏꜰ ʀᴀᴛᴇ ʟɪᴍɪᴛꜱ :)"%(60-(now - active_users[call.message.chat.id])))
                    return
            else:
                active_users[call.message.chat.id] = now
        def fn():
            playurl = 'https://youtube.com'+call.data.replace('hehe','')
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            _message = bot.send_message(chat_id=call.message.chat.id, text="𝚂𝚃𝙰𝚃𝚄𝚂 : 𝙵𝚎𝚝𝚌𝚑𝚒𝚗𝚐 𝚜𝚝𝚛𝚎𝚊𝚖𝚜")
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
                bot.edit_message_text(chat_id=_message.chat.id, message_id=_message.message_id, text="𝚂𝚃𝙰𝚃𝚄𝚂 : 𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍 𝚒𝚗 𝚙𝚛𝚘𝚐𝚛𝚎𝚜𝚜")
                try:
                    ydl.download(playurl)
                    bot.edit_message_text(chat_id=_message.chat.id, message_id=_message.message_id, text="𝚂𝚃𝙰𝚃𝚄𝚂 : 𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍 𝚌𝚘𝚖𝚙𝚕𝚎𝚝𝚎")
                except Exception as e:
                    bot.edit_message_text(chat_id=_message.chat.id, message_id=_message.message_id, text="`❗️ Exception occured`", parse_mode="Markdown")
                    data = f'ERROR WHILE DOWNLOADING URL\n\nURL : {playurl}\n{e}---------------------\n\n'
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
                    markupclose = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("❌ ᴄʟᴏꜱᴇ ᴘʟᴀʏᴇʀ ❌", callback_data="close"))
                    caption = f'{titleplay} | {authorplay}\n\n*Views* : {viewsplay}\n*Author* : {authorplay}\n*Published on* : {published_onplay}\n\n\n[Join MortyLabz](https://t.me/mortylab) | [Donate me](https://buymeacoffee.com/mortylabz)'
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
                InlineKeyboardButton("ꜰᴇᴇᴅʙᴀᴄᴋ", callback_data='feedback'),
                InlineKeyboardButton("ᴄʟᴏꜱᴇ", callback_data="close"))
            bot.send_message(call.message.chat.id, "_Mind giving me a feedback?_", parse_mode="Markdown", reply_markup=newmarkup)
        

        threading.Thread(target=fn).start()
       
    


    elif call.data == 'feedback':
        newwmarkup = InlineKeyboardMarkup(row_width=1)
        newwmarkup.add(
            InlineKeyboardButton("ᴄʟɪᴄᴋ ʜᴇʀᴇ", url='https://t.me/dailychannelsbot?start=morty_ai_bot'),
            InlineKeyboardButton("ᴄʟᴏꜱᴇ", callback_data="close"))
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=newwmarkup)

    elif call.data == 'close':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    elif 'video' in call.data:
        payloadvideo = call.data.replace('video', '').strip()
        markup = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("ʜɪɢʜ ʀᴇꜱᴏʟᴜᴛɪᴏɴ", callback_data=f"highres{payloadvideo}"), InlineKeyboardButton("ʟᴏᴡ ʀᴇꜱᴏʟᴜᴛɪᴏɴ", callback_data=f"lowres{payloadvideo}"), InlineKeyboardButton("﹤﹤ ʙᴀᴄᴋ", callback_data=f"home{payloadvideo}"))
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
            _message = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="𝚂𝚃𝙰𝚃𝚄𝚂 : 𝙵𝚎𝚝𝚌𝚑𝚒𝚗𝚐 𝚜𝚝𝚛𝚎𝚊𝚖𝚜")
            filenamevideo = f'videohigh-{str(randomNumber())}'
            ydl_optsvideo = {
                "format":"bestvideo[ext=ogg]+bestaudio[ext=mp3]/best",
                "outtmpl":filenamevideo+'.ogg',
                "geo_bypass":True,
                "quiet":True,
            }
            with YoutubeDL(ydl_optsvideo) as ydl:
                bot.edit_message_text(chat_id=_message.chat.id, message_id=_message.message_id, text="𝚂𝚃𝙰𝚃𝚄𝚂 : 𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍 𝚒𝚗 𝚙𝚛𝚘𝚐𝚛𝚎𝚜𝚜")
                try:
                    ydl.download(youtubevideourl) 
                    bot.edit_message_text(chat_id=_message.chat.id, message_id=_message.message_id, text="𝚂𝚃𝙰𝚃𝚄𝚂 : 𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍 𝚌𝚘𝚖𝚙𝚕𝚎𝚝𝚎")              
                except Exception as e:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="`❗️ Exception occured`", parse_mode="Markdown")
                    data = f'ERROR WHILE DOWNLOADING VIDEO\n\nURL : {youtubevideourl}\n{e}---------------------\n\n'
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
                            bot.send_video(chat_id=call.message.chat.id, video=videofile, caption=f"{title}\n\n\n[Join MortyLabz](https://t.me/mortylab) | [Donate me](https://buymeacoffee.com/mortylabz)", parse_mode="Markdown")
                            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

                except Exception as q:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="❗️ ERROR WHILE SENTING")
                    data3 = f'ERROR WHILE SENTING VIDEO\n\nURL : {youtubevideourl}\n{q}---------------------\n\n'
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
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("ʜɪɢʜᴇꜱᴛ Qᴜᴀʟɪᴛʏ", callback_data=f"dwaudio{payloadaudio}"), InlineKeyboardButton("﹤﹤ ʙᴀᴄᴋ", callback_data=f"home{payloadaudio}")))

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
            _message = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="𝚂𝚃𝙰𝚃𝚄𝚂 : 𝙵𝚎𝚝𝚌𝚑𝚒𝚗𝚐 𝚜𝚝𝚛𝚎𝚊𝚖𝚜")
            filenamevideolow = f'videolow-{str(randomNumber())}'
            ydl_optsvideolow = {
                "format":"worstvideo[ext=mp4]+worstaudio[ext=m4a]/worst",
                "outtmpl":filenamevideolow,
                "geo_bypass":True,
                "quiet":True,
            }
            with YoutubeDL(ydl_optsvideolow) as ydl:
                bot.edit_message_text(chat_id=_message.chat.id, message_id=_message.message_id, text="𝚂𝚃𝙰𝚃𝚄𝚂 : 𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍 𝚒𝚗 𝚙𝚛𝚘𝚐𝚛𝚎𝚜𝚜")
                try:
                    ydl.download(youtubevideourl)
                    bot.edit_message_text(chat_id=_message.chat.id, message_id=_message.message_id, text="𝚂𝚃𝙰𝚃𝚄𝚂 : 𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍 𝚌𝚘𝚖𝚙𝚕𝚎𝚝𝚎")
                except Exception as e:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="`❗️ Exception occured`", parse_mode="Markdown")
                    data5 = f'ERROR WHILE DOWNLOADING LOW VIDEO URL\n\nURL : {youtubevideourl}\n{e}---------------------\n\n'
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
                            bot.send_video(chat_id=call.message.chat.id,video=videofile,parse_mode='Markdown',  caption=f"{title}\n\n\n[Join MortyLabz](https://t.me/mortylab) | [Donate me](https://buymeacoffee.com/mortylabz)")
                            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

                except Exception as q:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="❗️ ERROR WHILE SENTING")
                    data6 = f'ERROR WHILE SENTING LOW VIDEO\n\nURL : {youtubevideourl}\n{q}---------------------\n\n'
                    with open('ytErrorLog.txt', 'a', encoding='utf-8') as file:
                        file.write(data6)
                        bot.send_message(call.message.chat.id, "❗️ ERROR HAS BEEN LOGGED")

                try:
                    os.remove(filenamevideolow+'.mp4')
                except:
                    print("ERROR WHILE DELETING")
        threading.Thread(target=fnlow).start()



    elif call.data.startswith('hgroup'):
        urlhigh = 'https://'+call.data.replace('hgroup', '').strip()
        now = datetime.datetime.now().timestamp()
        if call.message.from_user.id in active_users:
            if time_difference(active_users[call.message.from_user.id]):
                active_users[call.message.from_user.id] = now
            else:
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                bot.send_message(chat_id=call.message.chat.id, parse_mode="Markdown",disable_web_page_preview=True, text="*Downloads are limited to 1 download per 60 seconds* (%ds remaining)\n\n[Morty AI](https://t.me/morty_ai_bot)"%(60-(now - active_users[call.message.from_user.id])))
                return
        else:
            active_users[call.message.from_user.id] = now

        def downloadhigh():
            _message = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="𝚂𝚃𝙰𝚃𝚄𝚂 : 𝙵𝚎𝚝𝚌𝚑𝚒𝚗𝚐 𝚜𝚝𝚛𝚎𝚊𝚖𝚜")
            filenamevideogroup = f'videogrouphigh-{str(randomNumber())}'
            ydl_optsvideo = {
                "format":"bestvideo[ext=ogg]+bestaudio[ext=mp3]/best",
                "outtmpl":filenamevideogroup+'.ogg',
                "geo_bypass":True,
                "quiet":True,
            }
            with YoutubeDL(ydl_optsvideo) as ydl:
                bot.edit_message_text(chat_id=_message.chat.id, message_id=_message.message_id, text="𝚂𝚃𝙰𝚃𝚄𝚂 : 𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍 𝚒𝚗 𝚙𝚛𝚘𝚐𝚛𝚎𝚜𝚜")
                try:
                    ydl.download(urlhigh) 
                    bot.edit_message_text(chat_id=_message.chat.id, message_id=_message.message_id, text="𝚂𝚃𝙰𝚃𝚄𝚂 : 𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍 𝚌𝚘𝚖𝚙𝚕𝚎𝚝𝚎")              
                except Exception as e:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="`❗️ Exception occured`", parse_mode="Markdown")
                    data = f'ERROR WHILE DOWNLOADING VIDEO IN GROUP\n\nURL : {urlhigh}\n{e}---------------------\n\n'
                    with open('ytErrorLog.txt', 'a', encoding='utf-8') as file:
                        file.write(data)
                        bot.send_message(call.message.chat.id, "❗️ ERROR HAS BEEN LOGGED")



                try:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='⌛️')
                    if os.path.getsize(filenamevideogroup+'.ogg') >= 50000000:
                         bot.send_message(call.message.chat.id, "Filesize is too large to sent!")
                         bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                    else:
                        try:
                            html = requests.get(urlhigh).text
                            title = re.findall(r"<title>(.*?) - YouTube</title>", html)[0]
                        except:
                            title = 'Downloaded by Morty AI'

                        with open(filenamevideogroup+'.ogg', 'rb') as videofile:
                            bot.send_chat_action(call.message.chat.id, action="upload_video")
                            bot.send_video(chat_id=call.message.chat.id, video=videofile, caption=f"{title}\n\n\n[Join MortyLabz](https://t.me/mortylab) | [Donate me](https://buymeacoffee.com/mortylabz)", parse_mode="Markdown")
                            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

                except Exception as q:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="❗️ ERROR WHILE SENTING")
                    data3 = f'ERROR WHILE SENTING VIDEO TO GROUP\n\nURL : {urlhigh}\n{q}---------------------\n\n'
                    with open('ytErrorLog.txt', 'a', encoding='utf-8') as file:
                        file.write(data3)
                        bot.send_message(call.message.chat.id, "❗️ ERROR HAS BEEN LOGGED")
                
                try:
                    os.remove(filenamevideogroup+'.ogg')
                except:
                    print("ERROR WHILE DELETING")

        threading.Thread(target=downloadhigh).start()






    elif call.data.startswith('lgroup'):
        urllow = 'https://'+call.data.replace('lgroup', '').strip()
        now = datetime.datetime.now().timestamp()
        if call.message.from_user.id in active_users:
            if time_difference(active_users[call.message.from_user.id]):
                active_users[call.message.from_user.id] = now
            else:
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                bot.send_message(chat_id=call.message.chat.id, parse_mode="Markdown",disable_web_page_preview=True, text="*Downloads are limited to 1 download per 60 seconds* (%ds remaining)\n\n[Morty AI](https://t.me/morty_ai_bot)"%(60-(now - active_users[call.message.from_user.id])))
                return
        else:
            active_users[call.message.from_user.id] = now

        def downloadloww():
            _message = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="𝚂𝚃𝙰𝚃𝚄𝚂 : 𝙵𝚎𝚝𝚌𝚑𝚒𝚗𝚐 𝚜𝚝𝚛𝚎𝚊𝚖𝚜")
            filenamevideogrouplow = f'videogrouplow-{str(randomNumber())}'
            ydl_optsvideolow = {
                "format":"worstvideo[ext=mp4]+worstaudio[ext=m4a]/worst",
                "outtmpl":filenamevideogrouplow+'.mp4',
                "geo_bypass":True,
                "quiet":True,
            }
            with YoutubeDL(ydl_optsvideolow) as ydl:
                bot.edit_message_text(chat_id=_message.chat.id, message_id=_message.message_id, text="𝚂𝚃𝙰𝚃𝚄𝚂 : 𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍 𝚒𝚗 𝚙𝚛𝚘𝚐𝚛𝚎𝚜𝚜")
                try:
                    ydl.download(urllow) 
                    bot.edit_message_text(chat_id=_message.chat.id, message_id=_message.message_id, text="𝚂𝚃𝙰𝚃𝚄𝚂 : 𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍 𝚌𝚘𝚖𝚙𝚕𝚎𝚝𝚎")         
                except Exception as e:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="`❗️ Exception occured`", parse_mode="Markdown")
                    data = f'ERROR WHILE DOWNLOADING VIDEO IN GROUP\n\nURL : {urllow}\n{e}---------------------\n\n'
                    with open('ytErrorLog.txt', 'a', encoding='utf-8') as file:
                        file.write(data)
                        bot.send_message(call.message.chat.id, "❗️ ERROR HAS BEEN LOGGED")



                try:
                    
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='⌛️')
                    if os.path.getsize(filenamevideogrouplow+'.mp4') >= 50000000:
                         bot.send_message(call.message.chat.id, "Filesize is too large to sent!")
                         bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                    else:
                        try:
                            html = requests.get(urllow).text
                            title = re.findall(r"<title>(.*?) - YouTube</title>", html)[0]
                        except:
                            title = 'Downloaded by Morty AI'

                        with open(filenamevideogrouplow+'.mp4', 'rb') as videofilelow:
                            bot.send_chat_action(call.message.chat.id, action="upload_video")
                            bot.send_video(chat_id=call.message.chat.id, video=videofilelow, caption=f"{title}\n\n\n[Join MortyLabz](https://t.me/mortylab) | [Donate me](https://buymeacoffee.com/mortylabz)", parse_mode="Markdown")
                            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

                except Exception as q:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="❗️ ERROR WHILE SENTING")
                    data3 = f'ERROR WHILE SENTING VIDEO TO GROUP\n\nURL : {urllow}\n{q}---------------------\n\n'
                    with open('ytErrorLog.txt', 'a', encoding='utf-8') as file:
                        file.write(data3)
                        bot.send_message(call.message.chat.id, "❗️ ERROR HAS BEEN LOGGED")
                
                try:
                    os.remove(filenamevideogrouplow+'.mp4')
                except:
                    print("ERROR WHILE DELETING")

        threading.Thread(target=downloadloww).start()
        






    elif "home" in call.data:
        homepayload = call.data.replace("home", '').strip()
        homemarkup = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton("ᴠɪᴅᴇᴏ 📹", callback_data=f"video{homepayload}"), InlineKeyboardButton("ᴀᴜᴅɪᴏ 🎧", callback_data=f"audiores{homepayload}"), InlineKeyboardButton("❌ ᴄᴀɴᴄᴇʟ ❌", callback_data="close"))
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
            _message = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="𝚂𝚃𝙰𝚃𝚄𝚂 : 𝙵𝚎𝚝𝚌𝚑𝚒𝚗𝚐 𝚜𝚝𝚛𝚎𝚊𝚖𝚜")
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
                bot.edit_message_text(chat_id=_message.chat.id, message_id=_message.message_id, text="𝚂𝚃𝙰𝚃𝚄𝚂 : 𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍 𝚒𝚗 𝚙𝚛𝚘𝚐𝚛𝚎𝚜𝚜")
                try:
                    ydl.download(youtubevideourl)
                    bot.edit_message_text(chat_id=_message.chat.id, message_id=_message.message_id, text="𝚂𝚃𝙰𝚃𝚄𝚂 : 𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍 𝚌𝚘𝚖𝚙𝚕𝚎𝚝𝚎")
                except Exception as e:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="`❗️ Exception occured`", parse_mode="Markdown")
                    data = f'ERROR WHILE DOWNLOADING AUDIO\n\nURL : {youtubevideourl}\n{e}---------------------\n\n'
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
                        caption = f'{titleaudio}\n\n\n[Join MortyLabz](https://t.me/mortylab) | [Donate me](https://buymeacoffee.com/mortylabz)'
                        with open(filenameaudio+'.mp3', 'rb') as audiofile:
                            bot.send_audio(chat_id=call.message.chat.id,audio=audiofile, caption=caption, parse_mode='Markdown')
                            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                except Exception as n:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="❗️ ERROR WHILE SENTING")
                    data2 = f'ERROR WHILE SENTING YOUTUBE AUDIO\n\nURL : {youtubevideourl}\n{n}---------------------\n\n'
                    with open('ytErrorLog.txt', 'a', encoding='utf-8') as file:
                        file.write(data2)
                        bot.send_message(call.message.chat.id, "❗️ ERROR HAS BEEN LOGGED")

                try:
                    os.remove(filenameaudio+'.mp3')
                except:
                    print("ERROR WHILE DELETING")
        threading.Thread(target=fnaudio).start()
    elif call.data == 'usage':
        reply1 = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("﹤﹤ ʙᴀᴄᴋ", callback_data="acchom"))
        text = '━━━━━ ᴜꜱᴀɢᴇ ━━━━━\n\n★ 1 ɪᴍᴀɢᴇ = 3 ᴄʀᴇᴅɪᴛꜱ\n\n★ ɪꜰ ʏᴏᴜ ᴀʀᴇ ᴀ ꜱᴜʙꜱᴄʀɪʙᴇʀ 15 ᴄʀᴇᴅɪᴛꜱ ᴡɪʟʟ ʙᴇ ᴀᴅᴅᴇᴅ ᴛᴏ ʏᴏᴜʀ ᴀᴄᴄᴏᴜɴᴛ ᴅᴀɪʟʏ'
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=reply1)
    elif call.data == "acchom":
        markuppp = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton("ᴜꜱᴀɢᴇ", callback_data="usage"), InlineKeyboardButton("ᴄʟᴏꜱᴇ", callback_data="close"))
        msg = f'*━━━━━━ TOPUP ━━━━━━*\n\n*Topup from the list below, send the screenshot of proof* [here](https://t.me/ieatkidsforlunch) *for the redeem code.*\n\n*Use this code as* "`/topup Yourcode`" *to redeem your credits.*\n\nHere is the topup plans for credits:\n\n*1 ᴄʀᴇᴅɪᴛ              :   ₹29* ([ᴘᴀʏ ʜᴇʀᴇ](https://paytm.me/X-hCIVc))\n\n*3 Credits            :   ₹90* ([Pay here](https://paytm.me/oic-aio))\n\n*7 Credits            :   ₹210* ([Pay here](https://paytm.me/75-SJeJ))\n\n*16 Credits          :   ₹450* ([Pay here](https://paytm.me/9A9c-Ip))\n\n*30 Credits         :   ₹750* ([Pay here](https://paytm.me/DU9-cIp))\n\n*60 +5 Credits   :   ₹1450* ([Pay here](https://paytm.me/vr9-JeJ))'
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=msg, parse_mode="Markdown", disable_web_page_preview=True, reply_markup=markuppp)



@bot.message_handler(commands=['account'], chat_types=['group', 'supergroup'])
def no(message):
    bot.reply_to(message=message, text="ʏᴏᴜʀ ᴀᴄᴄᴏᴜɴᴛ ᴄᴀɴ ᴏɴʟʏ ʙᴇ ᴠɪᴇᴡᴇᴅ ɪɴ ᴘʀɪᴠᴀᴛᴇ ᴍᴇꜱꜱᴀɢᴇ")

# /ACCOUNT COMMAND
@bot.message_handler(commands=['account'], chat_types=['private'])
def account(message):
    userID = message.chat.id
    fetch = bot.send_message(userID, '⌛️')
    if collection_users.find_one({"id":str(userID)}):
        subscribed = 'No'
        if isSubscriber(userID) == 1:
            subscribed = 'Yes'
        p = collection_users.find_one({"id":str(userID)})
        total_credits = p['credits']
        joinedOn = datetime.datetime.fromtimestamp(p['joinedOn'])
        username = message.chat.username
        if message.chat.last_name:
            name = message.chat.first_name + " "+message.chat.last_name
        else:
            name = message.chat.first_name
        markup = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("ᴄʟᴏꜱᴇ", callback_data="close"))
        caption = f'*━━━ {name} ━━━*\n*╭━━━━━━━━━━━━━━╮*\n*﹄ ᴜꜱᴇʀɴᴀᴍᴇ* : @{username}\n*﹄ ᴜꜱᴇʀ ɪᴅ* : {userID}\n*﹄ ᴄʀᴇᴅɪᴛꜱ* : *{total_credits}*\n*﹄ ɪꜱ ꜱᴜʙꜱᴄʀɪʙᴇʀ* : {subscribed}\n*﹄ ʙɪᴏ* : {message.chat.bio}\n*﹄ ꜱᴛᴀʀᴛᴇᴅ ʙᴏᴛ ᴏɴ* : {str(joinedOn)[:10]}\n*╰━━━━━━━━━━━━━━╯*'
        photos = bot.get_user_profile_photos(user_id=userID, limit=1)
        if len(photos.photos) >= 1:
            for i in photos.photos:
                bot.delete_message(chat_id=message.chat.id, message_id=fetch.message_id)
                bot.send_photo(chat_id=message.chat.id, photo=i[0].file_id, caption=caption, parse_mode="Markdown", reply_markup=markup)
        else:
            with open('default.jpg', 'rb') as image:
                bot.delete_message(chat_id=message.chat.id, message_id=fetch.message_id)
                bot.send_photo(chat_id=message.chat.id, photo=image, caption=caption, parse_mode='Markdown', reply_markup=markup)
    else:
        bot.send_message(userID, "You do not have an account yet.\nSend /start to create one.")
        
    
    
    

@bot.message_handler(commands=['subscribe'], chat_types=['group', 'supergroup'])
def no(message):
    bot.reply_to(message=message, text="ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ᴄᴀɴ ᴏɴʟʏ ʙᴇ ᴜꜱᴇᴅ ɪɴ ᴘʀɪᴠᴀᴛᴇ ᴍᴇꜱꜱᴀɢᴇꜱ")


# /SUBSCRIBE COMMAND
@bot.message_handler(commands=['subscribe'], chat_types=['private'])
def subscribe_command(message):
    notSubscribed = True
    accessCode = message.text.replace('/subscribe', '')
    accessCode = accessCode.strip()
    if len(accessCode) == 0:
        bot.send_message(message.chat.id, "*ᴛᴏᴅᴀʏ'ꜱ ᴏꜰꜰᴇʀ - ₹99* ([ᴘᴀʏ ʜᴇʀᴇ](https://paytm.me/C6C-akp))\n\n*ᴘʀᴇᴍɪᴜᴍ ɢᴀɴɢ* - *USD 10$* ([ᴘᴀʏ ʜᴇʀᴇ](https://buymeacoffee.com/mortylabz/e/122212))\n\nꜱᴇɴᴅ ᴛʜᴇ ᴘʀᴏᴏꜰ [ʜᴇʀᴇ](https://t.me/ieatkidsforlunch) ᴛᴏ ɢᴇᴛ ᴛʜᴇ ᴀᴄᴄᴇꜱꜱ ᴄᴏᴅᴇ.\n\nᴜꜱᴇ ᴛʜɪꜱ ᴀᴄᴄᴇꜱꜱ ᴄᴏᴅᴇ ᴀꜱ\n'`/subscribe Youraccesscode`'\nᴛᴏ ɢᴇᴛ ᴘʀᴇᴍɪᴜᴍ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ\n\nꜱᴇɴᴅ '`/subscribe status`' ᴛᴏ ꜱᴇᴇ ʏᴏᴜʀ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ ꜱᴛᴀᴛᴜꜱ.\n\nʏᴏᴜ ᴡɪʟʟ ɢᴇᴛ:\n✅ - *15 ᴄʀᴇᴅɪᴛꜱ ᴅᴀɪʟʏ*\n✅ - *ɴᴏ ʀᴀᴛᴇ ʟɪᴍɪᴛꜱ ꜰᴏʀ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ*\n✅ - *ᴜʟᴛʀᴀ ʀᴇᴀʟɪꜱᴛɪᴄ 4ᴋ ɪᴍᴀɢᴇꜱ*\n✅ - *3x ꜰᴀꜱᴛᴇʀ ᴅᴏᴡɴʟᴏᴀᴅ ꜱᴘᴇᴇᴅ*\n✅ - *ᴊᴏɪɴ ᴏᴜʀ ᴍᴇɴ'ꜱ ɢᴀɴɢ 🗿*\n✅ - *ᴀɴᴅ ᴍᴀɴʏ ᴍᴏʀᴇ*", parse_mode='Markdown', disable_web_page_preview=True)
    elif accessCode == 'status':
        res = isSubscriber(message.chat.id)
        if res == 1:
            bot.send_message(message.chat.id, "*ꜱᴛᴀᴛᴜꜱ : ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀ*\n\nʏᴏᴜ ʜᴀᴠᴇ ᴀʟʟ ᴛʜᴇ ʙᴇɴᴇꜰɪᴛꜱ ɢʀᴀɴᴛᴇᴅ!", parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, "*ꜱᴛᴀᴛᴜꜱ : ꜰʀᴇᴇ ᴜꜱᴇʀ*\n\nꜱᴇɴᴅ /subscribe ᴛᴏ ꜱᴇᴇ ᴍᴏʀᴇ ᴅᴇᴛᴀɪʟꜱ ᴏɴ ʜᴏᴡ ᴛᴏ ʙᴇᴄᴏᴍᴇ ᴀ *ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀ*", parse_mode="Markdown")
    else:
        accessCode = accessCode.strip()
        userID = message.chat.id
        if subs_collection.find_one({"id":str(userID)}):
            notSubscribed = False
            bot.send_message(message.chat.id, "ʏᴏᴜ ᴀʀᴇ ᴀʟʀᴇᴀᴅʏ ꜱᴜʙꜱᴄʀɪʙᴇᴅ ᴛᴏ ᴘʀᴇᴍɪᴜᴍ. ᴇɴᴊᴏʏ ᴛʜᴇ ʙᴇɴᴇꜰɪᴛꜱ!")
        else:
            notSubscribed = True
        accepted = 0 # TRUE = 1 AND FALSE = 0
        if notSubscribed == True:
            tocheckcode = {'code':accessCode}
            if codes_collection.find_one(tocheckcode):
                bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
                subs_collection.insert_one({'id':str(userID)})
                bot.send_message(int(SUDO_ID), f"✅ @{str(message.chat.username)} has subscribed to Morty AI\n\nID : {str(message.chat.id)}")
                bot.send_message(message.chat.id, "✅ Congrats!!\nYou are subscribed to get acccess to many features. Enjoy your benefits.")
                codes_collection.delete_one({"code":accessCode})
            else:
                bot.send_message(userID, "❗️ᴛʜᴇ ᴀᴄᴄᴇꜱꜱ ᴄᴏᴅᴇ ᴡᴀꜱ ɪɴᴄᴏʀʀᴇᴄᴛ.")
            





# /BC COMMAND (OWNER)
@bot.message_handler(commands=['bc'], chat_types=['private'])
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
@bot.message_handler(commands=['reset'], chat_types=['private'])
def reset_data(message):
    if str(message.chat.id) == SUDO_ID:
        res = resetFile()
        if res == "200":
            bot.send_message(int(SUDO_ID), "users collection has been resetted!")


@bot.message_handler(commands=['topup'], chat_types=['group', 'supergroup'])
def no(message):
    bot.reply_to(message=message, text="ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ᴄᴀɴ ᴏɴʟʏ ʙᴇ ᴜꜱᴇᴅ ɪɴ ᴘʀɪᴠᴀᴛᴇ ᴍᴇꜱꜱᴀɢᴇꜱ")


# /TOPUP COMMAND
@bot.message_handler(commands=['topup'], chat_types=['private'])
def topup(message):
    userID = message.chat.id
    redeemcode = message.text.replace('/topup', '')
    if len(redeemcode) == 0:
        markup = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton("ᴜꜱᴀɢᴇ", callback_data="usage"), InlineKeyboardButton("ᴄʟᴏꜱᴇ", callback_data="close"))
        msg = f'*━━━━━━ ᴛᴏᴘᴜᴘ ━━━━━━*\n\n*ᴛᴏᴘᴜᴘ ꜰʀᴏᴍ ᴛʜᴇ ʟɪꜱᴛ ʙᴇʟᴏᴡ, ꜱᴇɴᴅ ᴛʜᴇ ꜱᴄʀᴇᴇɴꜱʜᴏᴛ ᴏꜰ ᴘʀᴏᴏꜰ* [ʜᴇʀᴇ](https://t.me/ieatkidsforlunch) *ꜰᴏʀ ᴛʜᴇ ʀᴇᴅᴇᴇᴍ ᴄᴏᴅᴇ.*\n\n*ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴅᴇ ᴀꜱ* "`/topup Yourcode`" *ᴛᴏ ʀᴇᴅᴇᴇᴍ ʏᴏᴜʀ ᴄʀᴇᴅɪᴛꜱ.*\n\nʜᴇʀᴇ ɪꜱ ᴛʜᴇ ᴛᴏᴘᴜᴘ ᴘʟᴀɴꜱ ꜰᴏʀ ᴄʀᴇᴅɪᴛꜱ:\n\n*1 ᴄʀᴇᴅɪᴛ               :  ₹29* ([ᴘᴀʏ ʜᴇʀᴇ](https://paytm.me/X-hCIVc))\n\n*3 ᴄʀᴇᴅɪᴛꜱ            :   ₹90* ([ᴘᴀʏ ʜᴇʀᴇ](https://paytm.me/oic-aio))\n\n*7 ᴄʀᴇᴅɪᴛꜱ            :   ₹210* ([ᴘᴀʏ ʜᴇʀᴇ](https://paytm.me/75-SJeJ))\n\n*16 ᴄʀᴇᴅɪᴛꜱ          :   ₹450* ([ᴘᴀʏ ʜᴇʀᴇ](https://paytm.me/9A9c-Ip))\n\n*30 ᴄʀᴇᴅɪᴛꜱ         :   ₹750* ([ᴘᴀʏ ʜᴇʀᴇ](https://paytm.me/DU9-cIp))\n\n*60 +5 ᴄʀᴇᴅɪᴛꜱ   :   ₹1450* ([ᴘᴀʏ ʜᴇʀᴇ](https://paytm.me/vr9-JeJ))'
        bot.send_message(userID, msg, parse_mode="Markdown", disable_web_page_preview=True, reply_markup=markup)
    else:
        redeemcode = redeemcode.strip()
        tocheck = {'code':redeemcode}
        userdat= collection_users.find_one({"id":str(userID)})
        dat = redeem_collection.find_one(tocheck)
        total_credits = userdat['credits']
        if dat:
            bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            total_credits = total_credits + dat['credits']
            collection_users.update_one({"id":str(userID)}, {'$set':{"credits":total_credits}})
            bot.send_message(userID, f"✅ Purchase successfull!\n\n*{dat['credits']} credits added to your account!*\n*Total credits : {collection_users.find_one({'id':str(userID)})['credits']}*", parse_mode="Markdown")
            redeem_collection.delete_one({"code":redeemcode})
            bot.send_message(int(SUDO_ID), f"✅ @{message.chat.username} just bought {dat['credits']} credits")
        else:
            bot.send_message(userID, '❗️ Invalid redeem code')




@bot.message_handler(commands=['img'], chat_types=['group', 'supergroup'])
def no(message):
    bot.reply_to(message=message, text="ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ᴄᴀɴ ᴏɴʟʏ ʙᴇ ᴜꜱᴇᴅ ɪɴ ᴘʀɪᴠᴀᴛᴇ ᴍᴇꜱꜱᴀɢᴇꜱ")

# /IMG COMMAND
@bot.message_handler(commands=['img'], chat_types=['private'])
def img_command(message):
   query = message.text.replace('/img', '')
   if len(query) == 0:
       
       bot.send_message(message.chat.id, "Use in '`/img query`' format\nExample :\n\n`/img An astronaut in the ocean`\n*1 image = 3 credits*", parse_mode='Markdown')
   else:
       userID = message.chat.id
       user = collection_users.find_one({"id":str(userID)})  
       if user:
            total_credits = user['credits']
            if total_credits <= 2:
                bot.send_message(chat_id=message.chat.id, parse_mode="Markdown",text=f"*Insufficent credits left on your account*\n\n*Credits needed : 3*\n*Credits left : {total_credits}*\n\nTopup some credits here /topup\nSubscribe to premium here /subscribe\nCheck account balance here /account")
            else:
                _message = bot.send_message(message.chat.id, "_Generating image . . ._", parse_mode="Markdown")
                response = generate_image(query, message)
                if response == 'err':
                    bot.delete_message(message.chat.id, _message.message_id)
                    bot.send_message(message.chat.id, "❗️ Some error occured")
                elif response == 'ratelimit':
                    bot.send_message(message.chat.id, RATELIMIT)
                elif response == 'forbidden':
                    bot.send_message(message.chat.id, FORBIDDEN)
                elif response == '500':
                    bot.send_message(message.chat.id, ERROR500)
                else:
                    bot.send_chat_action(chat_id=message.chat.id, action="upload_photo")
                 #    response['created']
                 #    images = response['images']
                    try:
                     #    for image in images:
                         bot.delete_message(message.chat.id, _message.message_id)
                         bot.send_photo(_message.chat.id, response,parse_mode='Markdown', caption="Generated by Morty AI\n\n\n[Join MortyLabz](https://t.me/mortylab) | [Donate me](https://buymeacoffee.com/mortylabz)")
                         total_credits = total_credits - 3
                         collection_users.update_one({"id":str(userID)}, {'$set':{"credits":total_credits}})
                    except Exception as e:
                        print(e)
                        bot.send_message(message.chat.id, "❗️ Some error occured")
       else:
           bot.send_message(userID, "You do not have an account yet.\nSend /start to create one.")
                
            




# /DEVELOPER COMMAND
@bot.message_handler(commands=['developer'])
def developer(message):
    keys = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Github", url="https://github.com/47hxl-53r"), InlineKeyboardButton("WhatsApp", url="https://wa.me/+918606672509"), InlineKeyboardButton("Telegram", url="https://t.me/ieatkidsforlunch"), InlineKeyboardButton("Buy me a coffee?", url="https://buymeacoffee.com/mortylabz"))
    bot.send_message(message.chat.id, "ᴛʜɪꜱ ʙᴏᴛ ɪꜱ ᴅᴇᴠᴇʟᴏᴘᴇᴅ ʙʏ ᴍᴏʀᴛʏ ʟᴀʙᴢ 🎀", reply_markup=keys)




# /COUNT COMMAND
@bot.message_handler(commands=['count'], chat_types=['private'])
def count_command(message):
    if str(message.chat.id) == SUDO_ID:
        resusers = collection_users.count_documents({})
        groups = groups_collection.count_documents({})
        ressubs = subs_collection.count_documents({})
        resfree = resusers - ressubs
        bot.send_message(int(SUDO_ID), f"Total users : {resusers}\nFree users : {resfree}\nPremium users : {ressubs}\nTotal Groups : {groups}")



# /ERRORS COMMAND (SUDO)
@bot.message_handler(commands=['errors'], chat_types=['private'])
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
@bot.message_handler(commands=['clearerrors'], chat_types=['private'])
def clearerrors_command(message):
    if str(message.chat.id) == SUDO_ID:
        with open('imgErrorLog.txt', 'w') as imgerrorfile:
            imgerrorfile.write("")
        with open('msgErrorLog.txt', 'w') as msgerrorfile:
            msgerrorfile.write("")
        with open('ytErrorLog.txt', 'w') as yterrorfile:
            yterrorfile.write("")
        bot.send_message(message.chat.id, "Error Logs cleared")


@bot.message_handler(commands=['youtube'], chat_types=['group', 'supergroup'])
def no(message):
    bot.reply_to(message=message, text="ɪɴ ɢʀᴏᴜᴘꜱ ʏᴏᴜ ᴄᴀɴ ꜱɪᴍᴘʟʏ ᴊᴜꜱᴛ ꜱᴇɴᴛ ᴛʜᴇ ᴠɪᴅᴇᴏ ᴜʀʟ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ.")


# /YOUTUBE COMMAND
@bot.message_handler(commands=['youtube'], chat_types=['private'])
def youtube_command(message):
    query = message.text.replace('/youtube', '')
    if len(query) == 0:
        bot.send_message(message.chat.id, "Use in `/youtube url` format\nExample:\n\n`/youtube https://youtu.be/dQw4w9WgXcQ`", parse_mode="Markdown")
    else:
        bot.delete_message(message.chat.id, message.message_id)
        youtubevideourl = query.strip()
        if isValid(youtubevideourl):
            payload = youtubevideourl.replace('https://youtu.be/', '').strip()
            markup = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton("ᴠɪᴅᴇᴏ 📹", callback_data= f"video{payload}"), InlineKeyboardButton("ᴀᴜᴅɪᴏ 🎧", callback_data=f"audiores{payload}"), InlineKeyboardButton("❌ ᴄᴀɴᴄᴇʟ ❌", callback_data="close"))
            bot.send_message(chat_id=message.chat.id,text=f"*URL : {youtubevideourl}*\n\n*Select an operation 👇*", reply_markup=markup, parse_mode="Markdown", disable_web_page_preview=True)
        else:
            bot.send_message(message.chat.id, "Invalid URL detected\n\nURL must start with `https://youtu.be/`", parse_mode="Markdown")



@bot.message_handler(commands=['scrape'], chat_types=['group', 'supergroup'])
def no(message):
    bot.reply_to(message=message, text="ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ᴄᴀɴ ᴏɴʟʏ ʙᴇ ᴜꜱᴇᴅ ɪɴ ᴘʀɪᴠᴀᴛᴇ ᴍᴇꜱꜱᴀɢᴇꜱ")


# /SCRAPE COMMAND
@bot.message_handler(commands=['scrape'], chat_types=['private'])
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
                    print(f"\n\n{e7}\n\n")
                    bot.send_message(message.chat.id, "❗️ Some error occured!")
                try:
                    # PHASE 3
                    os.remove(filename)
                except FileNotFoundError as fnf:
                    # PHASE 3 (EXCEPTION)
                    print(f"\n{fnf}\n")
        else:
            bot.send_message(message.chat.id, "❗️ Invalid URL detected")





# GROUP CHAT HANDLERS SECTION

@bot.message_handler(commands=['start'], chat_types=['group', 'supergroup'])
def start(message):
    bot.reply_to(message=message, text="ꜱᴇɴᴅ ᴍᴇ ᴀ ʟɪɴᴋ ᴛᴏ ᴀɴʏ ʏᴏᴜᴛᴜʙᴇ ᴠɪᴅᴇᴏ ᴀɴᴅ ɪ ᴡɪʟʟ ᴅᴏᴡɴʟᴏᴀᴅ ɪᴛ ꜰᴏʀ ʏᴏᴜ")

@bot.message_handler(content_types=['text'], chat_types=['group', 'supergroup'], text_startswith=('https://youtu.be', 'https://www.youtube.com', 'https://youtube.com','https://m.youtube.com'))
def reply(message):
    url = message.text
    markup = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("ʜɪɢʜ ʀᴇꜱᴏʟᴜᴛɪᴏɴ", callback_data=f"hgroup{url.replace('https://', '').strip()}"), InlineKeyboardButton("ʟᴏᴡ ʀᴇꜱᴏʟᴜᴛɪᴏɴ", callback_data=f'lgroup{url.replace("https://", "").strip()}'), InlineKeyboardButton("❌ ᴄʟᴏꜱᴇ ❌", callback_data="close"))  
    bot.send_message(message.chat.id, f"*Hey @{message.from_user.username}*\n*ꜱᴇʟᴇᴄᴛ ᴀɴ ᴏᴘᴇʀᴀᴛɪᴏɴ* 👇",parse_mode='Markdown', reply_markup=markup, disable_web_page_preview=True)



bot.add_custom_filter(custom_filters.TextStartsFilter())
    
    
    
# AI CHAT HANDLER (AI IS USED HERE)
# @bot.message_handler(commands=['msg'])
# def aiChatHandlerFunction(message):
#    query = message.text.lower().replace('/msg', '').replace("sex", '').replace("fuck", '')
#    if len(query) == 0:
#        bot.send_message(message.chat.id, "Sent in '`/msg query`' format\nExample :\n\n`/msg How to make a pizza?`", parse_mode='Markdown')
#    else:
#        userId = message.chat.id
#        user = collection_users.find_one({"id":str(userId)})
#        total_credits = user['credits']
#        if total_credits == 0:
#            bot.send_message(chat_id=message.chat.id, parse_mode="Markdown",text=f"*Insufficent credits left*\n\n*Credits needed : 1*\n*Credits left : {total_credits}*\n\nTopup some credits here /topup\nSubscribe to premium here /subscribe")
#        else:
#            bot.send_chat_action(chat_id=message.chat.id, action="typing")
#            query = query.strip()
#            ai_response = askAI(query)
#            if ai_response == 'ratelimit':
#                bot.send_message(message.chat.id, RATELIMIT)
#            elif ai_response == '500':
#                bot.send_message(message.chat.id, ERROR500)
#            elif ai_response == None:
#                bot.send_message(message.chat.id, "❗️ Some error occured")
#            else:
#                bot.send_message(message.chat.id, ai_response)
#                total_credits = total_credits - 1
#                collection_users.update_one({"id":str(userId)}, {'$set':{"credits":total_credits}})
          
 


bot.infinity_polling()






