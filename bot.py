import telebot, datetime, os, time, re, requests, threading, shutil, subprocess
from wikipedia import wikipedia
from telebot.storage import StateMemoryStorage
from settings import *
from insta import *
from wikipedia.exceptions import PageError, DisambiguationError
from yt_dlp import YoutubeDL
from icrawler.builtin import GoogleImageCrawler
from telebot import custom_filters
from telebot.apihelper import ApiTelegramException
from pymongo import MongoClient
from youtube_search import YoutubeSearch
from functions import resetFile, sourcecode, isValid, randomNumber, isSubscriber, FORBIDDEN, isIgLink, isFbLink, get_stats, split_video
from dotenv import load_dotenv, find_dotenv
from telebot.handler_backends import State, StatesGroup
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
BOT_STARTED = time.time()


load_dotenv(find_dotenv())
TELE_API_KEY = os.getenv('TELE_API_KEY')
SUDO_ID = os.getenv('SUDO_ID')
BOT_USERNAME = 'morty_ai_bot'
# BOT_USERNAME = 'nigganibbabot'
# BOT_USERNAME = 'atulrvbot'


telebot.apihelper.READ_TIMEOUT = 350
telebot.apihelper.API_URL = 'http://0.0.0.0:7676/bot{0}/{1}'

state_storage = StateMemoryStorage()
class MyStates(StatesGroup):
    settings = State()
    youtube = State()
    play = State()
    maxcount = State()



cluster = MongoClient("mongodb+srv://tzvri75136:Atulrv2005@mortydb.t0mwlvs.mongodb.net/?retryWrites=true&w=majority")
db = cluster['mortydb']
collection_users = db['users']
subs_collection = db['subscribers']
igerrorlogs_collection = db['igerrorlogs']
codes_collection = db['Accesscodes'] 
redeem_collection = db['redeemcodes']
groups_collection = db['groups']
yterrorlogs_collection = db['yterrorlogs']
imgerrorlogs_collection = db['imgerrorlogs']



# INITIALISING THE BOT WITH TELEGRAM API
bot = telebot.TeleBot(TELE_API_KEY, threaded=True, state_storage=state_storage)
active_users = {}
active_users_wiki = {}
play_active_users = {}
bot.delete_my_commands(scope=telebot.types.BotCommandScopeAllGroupChats(), language_code=None)



bot.set_my_commands(commands=[
    telebot.types.BotCommand("start", 'To start me'),
    telebot.types.BotCommand("play", "Play any music"),
    telebot.types.BotCommand("yt", "Download youtube media"),
    telebot.types.BotCommand("ig", "Download Instagram media"),
    telebot.types.BotCommand("fb", "Download Facebook media"),
    telebot.types.BotCommand("img", "Get any image you want"),
    telebot.types.BotCommand("wiki", "Search wikipedia"),
    telebot.types.BotCommand("ping", "Test my speed"),
    telebot.types.BotCommand("stats", "Server status"),
    telebot.types.BotCommand("scrape", "Scrape a website"),
    telebot.types.BotCommand("account", "View your account"),
    telebot.types.BotCommand("join", "Join our basements"),
    telebot.types.BotCommand("developer", "View developer info")
], scope=telebot.types.BotCommandScopeAllGroupChats())


bot.set_my_commands(commands=[
    telebot.types.BotCommand("start", 'To start me'),
    telebot.types.BotCommand("settings", 'Manage settings of the bot'),
    telebot.types.BotCommand("play", "Play any music"),
    telebot.types.BotCommand("yt", "Download youtube media"),
    telebot.types.BotCommand("ig", "Download Instagram media"),
    telebot.types.BotCommand("fb", "Download Facebook media"),
    telebot.types.BotCommand("img", "Get any image you want"),
    telebot.types.BotCommand("wiki", "Search wikipedia"),
    telebot.types.BotCommand("ping", "Test my speed"),
    telebot.types.BotCommand("stats", "Server status"),
    telebot.types.BotCommand("scrape", "Scrape a website"),
    telebot.types.BotCommand("account", "View your account"),
    telebot.types.BotCommand("join", "Join our basements"),
    telebot.types.BotCommand("developer", "View developer info")
], scope=telebot.types.BotCommandScopeAllChatAdministrators())


# FUNCTION TO SEARCH VIDEO AND RETURN DICTIONARY OF TITLE AND CORRESPONDING URL
def searchVideo(title, max_results):
    data = {}
    resultsvid = YoutubeSearch(title, max_results=max_results).to_dict()
    for i in resultsvid[0:]:
        data.update({f'{i["title"]}':f'{i["url_suffix"]}'})
    return data
    


def time_difference(last):
    current_time = datetime.datetime.now().timestamp()
    if (current_time - last) > 60:
        return True
    else:
        return False 
    



def time_difference_wiki(last):
    current_time = datetime.datetime.now().timestamp()
    if (current_time - last) > 20:
        return True
    else:
        return False 






# /IG COMMAND PRIVATE
@bot.message_handler(commands=['ig'], chat_types=['private'])
def download_ig(message):
    query = message.text.replace('/ig', '').strip()
    userID = message.chat.id
    if len(query) == 0:
        bot.send_message(userID, 'ꜱᴇɴᴛ ɪɴ `/ig URL` ꜰᴏʀᴍᴀᴛ\n\nᴇxᴀᴍᴘʟᴇ:\n\n`/ig https://www.instagram.com/reel/Cp5VHXNDTqF/?utm_source=ig_web_copy_link`\n\nᴛʜɪꜱ ꜰᴇᴀᴛᴜʀᴇ ɪꜱ ɴᴏᴛ ꜱᴜᴘᴘᴏʀᴛᴇᴅ ᴡɪᴛʜ ꜱᴛᴏʀɪᴇꜱ ʏᴇᴛ.', parse_mode='Markdown')
    else:
        def private():
            if not isIgLink(query):
                bot.send_message(userID, 'ɪɴᴠᴀʟɪᴅ ɪɴꜱᴛᴀɢʀᴀᴍ ᴜʀʟ ᴅᴇᴛᴇᴄᴛᴇᴅ, ᴛʀʏ ᴀɢᴀɪɴ!')
            else:
                msg = "🔎"
                caption = 'ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ʙʏ ᴍᴏʀᴛʏ ᴀɪ\n\n[Join MortyLabz](https://t.me/mortylab) | [Donate me](https://buymeacoffee.com/mortylabz)'
                if isSubscriber(userID) == 0:
                    now = datetime.datetime.now().timestamp()
                    if userID in active_users:
                        if time_difference(active_users[userID]):
                            active_users[userID] = now
                        else:
                            bot.delete_message(chat_id=userID, message_id=message.message_id)
                            bot.send_message(chat_id=userID, parse_mode="Markdown", text="*ᴅᴏᴡɴʟᴏᴀᴅꜱ ᴀʀᴇ ʟɪᴍɪᴛᴇᴅ ᴛᴏ 1 ᴅᴏᴡɴʟᴏᴀᴅ ᴘᴇʀ 60 ꜱᴇᴄᴏɴᴅꜱ* (%dꜱ ʀᴇᴍᴀɪɴɪɴɢ)\n\n/subscribe ᴛᴏ ɢᴇᴛ ʀɪᴅ ᴏꜰ ʀᴀᴛᴇ ʟɪᴍɪᴛꜱ :)"%(60-(now - active_users[userID])))
                            return
                    else:
                        active_users[userID] = now

                if query.startswith('https://www.instagram.com/reel/') or query.startswith('https://instagram.com/reel/'):
                    bot.delete_message(userID, message.message_id)
                    _messag = bot.send_message(userID, msg)
                    video = igreel(query)
                    bot.delete_message(userID, _messag.message_id)
                    bot.send_chat_action(chat_id=userID, action="upload_video")
                    try:
                        bot.send_video(userID, video=video, caption=caption, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("Open in Instagram", url=query)))
                    except ApiTelegramException as exception:
                        try:
                            video2 = igreel2(query)
                            bot.send_video(userID, video=video2, caption=caption, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("Open in Instagram", url=query)))
                        except Exception as e:
                            towrite = {'URL':query, 'ERROR':str(e)}
                            igerrorlogs_collection.insert_one(towrite)
                            bot.send_message(userID, "Exception occured")  

            
                elif query.startswith('https://www.instagram.com/p/') or query.startswith('https://instagram.com/p/'):
                    bot.delete_message(userID, message.message_id)
                    _message = bot.send_message(userID, msg, parse_mode='Markdown')
                    medias = igphoto(query)
                    if len(medias) == 0:
                        bot.delete_message(userID, _message.message_id)
                        bot.send_message(chat_id=userID, text=f'ꜱᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ\n\n<b>ONLY WORKS WITH POSTS ON PUBLIC ACCOUNT</b>\n\nᴄᴏᴘʏ ᴛʜᴇ ʙᴇʟᴏᴡ ᴍᴇꜱꜱᴀɢᴇ ᴀɴᴅ ʀᴇᴘᴏʀᴛ ᴛʜɪꜱ ʙᴜɢ <a href="https://t.me/ieatkidsforlunch">ʜᴇʀᴇ</a>\n\n<code>ERROR CODE : 1-photo-private\nID : {userID}\nIs subscriber : {str(isSubscriber(userID))}\nTime : {str(datetime.datetime.now())}\nURL: {query}</code>', parse_mode='HTML', disable_web_page_preview=True)
                    else:
                        bot.delete_message(userID, _message.message_id)
                
                        for i in medias:
                            if i.startswith('##photo##'):
                                try:
                                    bot.send_photo(userID, photo=i.replace('##photo##', '').strip(), caption=caption, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("Open in Instagram", url=query)))
                                except ApiTelegramException as exception:
                                    bot.send_message(userID, "Exception occured")
                                    towrite = {'URL':query, 'ERROR':str(exception)}
                                    igerrorlogs_collection.insert_one(towrite)

                            else:
                                try:
                                    bot.send_video(userID, video=i.replace('##video##', '').strip(), caption=caption, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("Open in Instagram", url=query)))
                                except ApiTelegramException as e2:
                                    bot.send_message(userID, "Exception occured")
                                    towrite3 = {'URL':query, 'ERROR':str(e2)}
                                    igerrorlogs_collection.insert_one(towrite3)

        threading.Thread(target=private).start()








@bot.message_handler(commands=['ping'], chat_types=['group', 'supergroup', 'private'])
def stats_command(message):
    chatID = message.chat.id
    _start = time.time()
    msg = bot.reply_to(message=message, text="wait")
    _end = time.time()
    ping = int((_end - _start) * 1000)
    uptime_seconds = int(time.time() - BOT_STARTED)
    hours = uptime_seconds // 3600
    minutes = (uptime_seconds % 3600) // 60
    seconds = (uptime_seconds % 60)
    uptime_str = f"{hours}ʜ:{minutes}ᴍ:{seconds}ꜱ"
    reply = f"*【 ＰＯＮＧ 】*\n\n⚡️ *ᴍᴏʀᴛʏᴀɪ ɪꜱ ᴀʟɪᴠᴇ*\n⚡️ *ᴛɪᴍᴇ ᴛᴀᴋᴇɴ : {ping}ᴍꜱ*\n⚡️ *ᴜᴘᴛɪᴍᴇ : {uptime_str}*"
    bot.edit_message_text(chat_id=chatID,message_id=msg.message_id, text=reply, parse_mode='Markdown')




@bot.message_handler(['stats'])
def stats(message):
    msg = bot.send_message(message.chat.id, text='_Fetching . . ._', parse_mode='Markdown')
    bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id,text=get_stats(), parse_mode='html', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("❌ ᴄʟᴏꜱᴇ ❌", callback_data='close')))
    



# /IG COMMAND GROUP
@bot.message_handler(content_types=['text'], chat_types=['group', 'supergroup'], text_startswith=('https://www.instagram.com/', 'https://instagram.com/'))
def ig_group(message):
    userID = message.chat.id
    if groups_collection.find_one({'id':str(userID)})['general']['clean_mode'] == 'on':
        try:
            bot.delete_message(userID, message.message_id)
        except:
            pass

 
    def group():
        config_chataction = groups_collection.find_one({'id':str(userID)})['general']['chat_action']
        url = message.text
        now = datetime.datetime.now().timestamp()
        if message.from_user.id in active_users:
            if time_difference(active_users[message.from_user.id]):
                active_users[message.from_user.id] = now
            else:
                bot.send_message(chat_id=userID,parse_mode="Markdown",disable_web_page_preview=True, text="*Downloads are limited to 1 download per 60 seconds* (%ds remaining)\n\n[Morty AI](https://t.me/morty_ai_bot)"%(60-(now - active_users[message.from_user.id])))
                return
        else:
            active_users[message.from_user.id] = now 

        downloading = '🔎'
        caption = 'ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ʙʏ ᴍᴏʀᴛʏ ᴀɪ\n\n[Join MortyLabz](https://t.me/mortylab) | [Donate me](https://buymeacoffee.com/mortylabz)'
        if url.startswith('https://www.instagram.com/reel/') or url.startswith('https://instagram.com/reel/'):
            _messagereel = bot.send_message(userID, downloading, parse_mode='Markdown')
            video = igreel(url)
            if config_chataction == 'on':
                bot.send_chat_action(chat_id=userID, action="upload_video")
            if video == 'error':
                bot.send_message(userID, f'ꜱᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ\n\n<b>ONLY WORKS WITH POSTS ON PUBLIC ACCOUNT</b>\n\nᴄᴏᴘʏ ᴛʜᴇ ʙᴇʟᴏᴡ ᴍᴇꜱꜱᴀɢᴇ ᴀɴᴅ ʀᴇᴘᴏʀᴛ ᴛʜɪꜱ ʙᴜɢ <a href="https://t.me/ieatkidsforlunch">ʜᴇʀᴇ</a>\n\n<code>ERROR CODE : 1-reel-group\nID : {userID}\nTime : {str(datetime.datetime.now())}\nURL: {url}</code>', parse_mode='HTML', disable_web_page_preview=True)
            else:
                bot.delete_message(userID, _messagereel.message_id)
                try:
                    bot.send_video(userID, video=video, caption=caption, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("Open in Instagram", url=url)))
                except ApiTelegramException as e:
                    try:
                        video2 = igreel2(url)
                        bot.send_video(userID, video=video2, caption=caption, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("Open in Instagram", url=url)))
                    except Exception as e:
                        towrite = {'URL':url, 'ERROR':str(e)}
                        igerrorlogs_collection.insert_one(towrite)
                        bot.send_message(userID, "Exception occured")  


        elif url.startswith('https://www.instagram.com/p/') or url.startswith('https://instagram.com/p/'):
            _messagephoto = bot.send_message(userID, downloading, parse_mode='Markdown')
            medias = igphoto(url)
            if len(medias) == 0:
                bot.delete_message(userID, _messagephoto.message_id)
                bot.send_message(userID, f'ꜱᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ\n\n<b>ONLY WORKS WITH POSTS ON PUBLIC ACCOUNT</b>\n\nᴄᴏᴘʏ ᴛʜᴇ ʙᴇʟᴏᴡ ᴍᴇꜱꜱᴀɢᴇ ᴀɴᴅ ʀᴇᴘᴏʀᴛ ᴛʜɪꜱ ʙᴜɢ <a href="https://t.me/ieatkidsforlunch">ʜᴇʀᴇ</a>\n\n<code>ERROR CODE : 1-photo-group\nID : {userID}\nTime : {str(datetime.datetime.now())}\nURL: {url}</code>', parse_mode='HTML', disable_web_page_preview=True)
            else:
                bot.delete_message(userID, _messagephoto.message_id)
                for i in medias:

                    if i.startswith('##photo##'):
                        if config_chataction == 'on':
                            bot.send_chat_action(chat_id=userID, action="upload_photo")
                        bot.send_photo(userID, photo=i.replace('##photo##', '').strip(), caption=caption, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("Open in Instagram", url=url)))
                    else:
                        if config_chataction == 'on':
                            bot.send_chat_action(chat_id=userID, action="upload_video")
                        bot.send_video(userID, video=i.replace('##video##', '').strip(), caption=caption, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("Open in Instagram", url=url)))
        else:
            bot.send_message(userID, 'ɪɴᴠᴀʟɪᴅ ɪɴꜱᴛᴀɢʀᴀᴍ ʀᴇᴇʟ/ᴘʜᴏᴛᴏ ᴜʀʟ')
    threading.Thread(target=group).start()

        
        

    




def generate_image(query, message, total_credits, userID):
    def download(query, message, total_credits, userID):
        try:
            _message = bot.send_message(chat_id=message.chat.id, text=f"_Searching for {query.strip().capitalize()}. . ._", parse_mode='Markdown')
            file_dir_sub = f'{str(userID).replace("-", "").strip()}'
            try:
                crawler = GoogleImageCrawler(storage={'root_dir':f'./{file_dir_sub}'})
                crawler.crawl(keyword=query, max_num=2)
            except Exception as exception:
                towrite1 = {'PROMPT':query, 'ERROR':str(exception)}
                imgerrorlogs_collection.insert_one(towrite1)

            caption = f'<b>{query.capitalize()}</b>\n\n<a href="https://t.me/mortylab">Join MortyLabz</a> | <a href="https://buymeacoffee.com/mortylabz">Donate me</a>'
            filename = os.listdir(f'./{file_dir_sub}')[0]
            sent_id = message.chat.id
            error = False
            if message.chat.type == 'group' or message.chat.type == 'supergroup':
                chat_action = groups_collection.find_one({'id':str(message.chat.id)})['general']['chat_action'] == 'on'
            else:
                chat_action = True
            full_path = f'./{file_dir_sub}/{filename}'
            
            if chat_action:
                bot.send_chat_action(chat_id=message.chat.id, action="upload_photo")
            
            file_uri = 'file://' + os.path.abspath(os.path.join(os.getcwd(), full_path[2:]))
            bot.delete_message(chat_id=message.chat.id, message_id=_message.message_id)
            try:
                bot.send_photo(chat_id=sent_id, photo=file_uri, caption=caption, parse_mode='html')
                total_credits = total_credits - 2
                collection_users.update_one({"id":str(userID)}, {'$set':{"credits":total_credits}})
            except:
                error = True

            if error == True:
                filename = os.listdir(f'./{file_dir_sub}')[1]
                send_id = message.chat.id
                full_path = f'./{file_dir_sub}/{filename}'
                file_uri_sub = 'file://' + os.path.abspath(os.path.join(os.getcwd(), full_path[2:]))
                if chat_action:
                    bot.send_chat_action(chat_id=message.chat.id, action='upload_photo')
               
                try:
                    bot.send_photo(chat_id=send_id, photo=file_uri_sub, caption=caption, parse_mode='html')
                    total_credits = total_credits - 2
                    collection_users.update_one({'id':str(userID)}, {'$set':{"credits":total_credits}})
                except Exception as t:
                    bot.send_message(chat_id=sent_id, text="Exception occured while senting!")
                    towrite = {'PROMPT':query, 'ERROR':str(t)}
                    imgerrorlogs_collection.insert_one(towrite)
            try:
                shutil.rmtree(path=file_dir_sub)
            except Exception as error:
                towrite2 = {'PROMPT':query, 'ERROR':str(error)}
                imgerrorlogs_collection.insert_one(towrite2)


        except Exception as e:
            towrite = {"PROMPT":query, "ERROR":str(e)}
            imgerrorlogs_collection.insert_one(towrite)
            bot.send_message(message.chat.id, "❗️ Some error occured")

    threading.Thread(target=download, args=(query, message, total_credits, userID)).start()






@bot.my_chat_member_handler()
def me(message: telebot.types.ChatMemberUpdated):
    update = message.new_chat_member
    if update.status == 'member':
        if message.chat.type == 'group' or message.chat.type == 'supergroup' or message.chat.type == 'channel':
            bot.send_message(message.chat.id, "King is here!! HHAHAHAHA!!\n\nMake me an admin and i can start doing my job\n\nSend any youtube video URLs to download.\nSent any Instagram media URLs to download.\nSend any Facebook media URLs to download\nSend `/play songname` to play any song you like.\nSend `/wiki query` to get wikipedia results.")
            add_entry(message.chat.id)
        else:
            collection_users.insert_one({'id':str(message.chat.id)})
            bot.send_message(message.chat.id, f"Welcome back @{message.from_user.username}")
    if update.status == 'administrator':
        bot.send_message(message.chat.id, "Send any YouTube video URLs to download.\n\nSent any Instagram media URLs to download\n\nUse `/play any song` to play any song you want.\n\nSend any Facebook media URLs to download\n\nSend /wiki to get wikipedia search results\n\nSend /account to view your account", parse_mode="Markdown")
        add_entry(message.chat.id)

    if update.status == 'left':
        groups_collection.delete_one({"id":str(message.chat.id)})
    if update.status == 'kicked':
        collection_users.delete_one({'id':str(message.chat.id)})





@bot.message_handler(commands=['listdir'], chat_types=['private'])
def listdir(message):
    if message.chat.id == int(SUDO_ID):
        dirs = os.listdir('.')
        for i in dirs:
            if not i.startswith('.') or not i.startswith('_'):
                bot.send_message(int(SUDO_ID), i)



@bot.message_handler(commands=['start'], chat_types=['private'])
def start_message(message):
    userID = message.chat.id
    usermsg = message.message_id
    bot.delete_message(chat_id=userID, message_id=usermsg)
    bot.send_message(userID, "ᴍᴏʀᴛʏ ᴀɪ ʙᴏᴛ ɪꜱ ᴀ ᴄʜᴀᴛʙᴏᴛ ᴛʜᴀᴛ ᴘʀᴏᴠɪᴅᴇꜱ ᴀ ʀᴀɴɢᴇ ᴏꜰ ꜱᴇʀᴠɪᴄᴇꜱ ᴛᴏ ʜᴇʟᴘ ᴘᴇᴏᴘʟᴇ ᴍᴀɴᴀɢᴇ ᴛʜᴇɪʀ ᴅᴀʏ-ᴛᴏ-ᴅᴀʏ ᴛᴀꜱᴋꜱ. It can help you with tasks such as:\n\n🔰 *ɢᴇᴛ ɪᴍᴀɢᴇ ꜰʀᴏᴍ Qᴜᴇʀʏ*\n🔰 *ʏᴏᴜᴛᴜʙᴇ ᴠɪᴅᴇᴏ/ᴀᴜᴅɪᴏ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ*\n🔰 *ᴍᴜꜱɪᴄ ᴘʟᴀʏᴇʀ*\n🔰 *ɪɴꜱᴛᴀɢʀᴀᴍ ᴍᴇᴅɪᴀ ᴅᴏᴡɴʟᴏᴀᴅ*\n🔰 *ꜰᴀᴄᴇʙᴏᴏᴋ ᴍᴇᴅɪᴀ ᴅᴏᴡɴʟᴏᴀᴅ*\n🔰 *ᴡᴇʙ ꜱᴄʀᴀᴘɪɴɢ*\n🔰 *ꜱᴇᴀʀᴄʜ ᴡɪᴋɪᴘᴇᴅɪᴀ*\n🔰 *ᴀɴᴅ ᴍᴏʀᴇ.*\n\nᴛᴏ ɢᴇᴛ ꜱᴛᴀʀᴛᴇᴅ, ꜱɪᴍᴘʟʏ ꜱᴇɴᴅ ᴀ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ᴍᴏʀᴛʏ ᴀɪ ᴀɴᴅ ɪᴛ ᴡɪʟʟ ʀᴇꜱᴘᴏɴᴅ ᴡɪᴛʜ ᴛʜᴇ ʜᴇʟᴘ ʏᴏᴜ ɴᴇᴇᴅ.\n\n*⚠️ BASIC COMMANDS ⚠️*\n/img - ᴛᴏ ɢᴇᴛ ɪᴍᴀɢᴇ\n/play - ᴛᴏ ᴘʟᴀʏ ᴀɴʏ ᴍᴜꜱɪᴄ\n/yt - ᴅᴏᴡɴʟᴏᴀᴅ ʏᴏᴜᴛᴜʙᴇ ᴠɪᴅᴇᴏ/ᴀᴜᴅɪᴏ\n/ig - ɪɴꜱᴛᴀɢʀᴀᴍ ᴍᴇᴅɪᴀ ᴅᴏᴡɴʟᴏᴀᴅ\n/fb - ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ꜰᴀᴄᴇʙᴏᴏᴋ ᴍᴇᴅɪᴀ\n/wiki - ᴛᴏ ꜱᴇᴀʀᴄʜ ᴡɪᴋɪᴘᴇᴅɪᴀ\n/subscribe - ꜱᴜʙꜱᴄʀɪʙᴇ ᴛᴏ ᴘʀᴇᴍɪᴜᴍ\n/scrape - ᴡᴇʙ ꜱᴄʀᴀᴘɪɴɢ\n/join - ᴊᴏɪɴ ᴏᴜʀ ʙᴀꜱᴇᴍᴇɴᴛꜱ\n/developer - ᴅᴇᴠᴇʟᴏᴘᴇʀ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ", parse_mode='Markdown', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("❌ ᴄʟᴏꜱᴇ ❌", callback_data='close')))
    res = collection_users.find_one({"id":str(userID)})
    if not res:
        towrite = {'id':str(userID), "credits":4, "joinedOn":datetime.datetime.now().timestamp()}
        collection_users.insert_one(towrite)




@bot.message_handler(commands=['clean'], chat_types=['private'])
def clean(message):
    if message.chat.id == int(SUDO_ID):
        cleaned = 0
        files = os.listdir('.')
        for i in files:
            if i.startswith("play") or i.startswith("audio") or i.startswith("video") or i.startswith('error') or i.startswith('16'):
                os.remove(i)
                cleaned = cleaned + 1
    if cleaned == 0:
        bot.send_message(int(SUDO_ID), "Dir is empty, nothing to clean")
    else:
        bot.send_message(int(SUDO_ID), f'Cleaned {cleaned} files from directory.')






@bot.message_handler(commands=['sub'], chat_types=['private'])
def sub(message):
    if message.chat.id == int(SUDO_ID):
        command = message.text.replace('/sub', '').strip()
        if len(command) == 0:
            if subs_collection.find_one({'id':SUDO_ID}):
                bot.send_message(int(SUDO_ID), 'You are a subscriber')
            else:
                bot.send_message(int(SUDO_ID), 'You are not a subscriber')
        if command.lower() == 'true':
            subs_collection.insert_one({'id':SUDO_ID})
            collection_users.update_one({'id':str(SUDO_ID)}, {'$set':{'credits':100}})
            bot.send_message(int(SUDO_ID), 'Added as a subscriber')
        elif command.lower() == 'false':
            subs_collection.delete_one({'id':SUDO_ID})
            bot.send_message(int(SUDO_ID), "Removed from subscribers")
        else:
            bot.send_message(int(SUDO_ID), "It must be true or false")






@bot.message_handler(['codes'], chat_types=['private'])
def data(message):
    if str(message.chat.id) == SUDO_ID:
        with open('codes.txt', 'w') as f:
            f.write("----- SUBSCRIPTION CODES -----\n\n")
            for i in codes_collection.find({}):
                subscode = i['code']
                f.write(subscode+'\n')

            f.write("\n\n----- REDEEM CODES -----\n\n")
            for p in redeem_collection.find({}):
                redeemcode = f"{p['code']} : {p['credits']} credits\n"
                f.write(redeemcode)

        with open('codes.txt', 'r') as f2:
            bot.send_document(chat_id=int(SUDO_ID), document=f2)
        os.remove('codes.txt')
            
    




@bot.message_handler(commands=['join'], chat_types=['private'])
def join(message):
    markupjoin = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("ᴊᴏɪɴ ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ", url="https://t.me/+_FoaeZ-tvIQ4OGE9"), InlineKeyboardButton("ᴊᴏɪɴ ᴏꜰꜰɪᴄɪᴀʟ ᴄʜᴀɴɴᴇʟ", url="https://t.me/mortylab"), InlineKeyboardButton("🗿 ᴊᴏɪɴ ᴍᴇɴ'ꜱ ɢᴀɴɢ 🗿", callback_data="checkpremium"))
    bot.send_message(message.chat.id, "Get support from here", reply_markup=markupjoin)






@bot.message_handler(commands=['join'], chat_types=['group', 'supergroup'])
def join(message):
    if groups_collection.find_one({'id':str(message.chat.id)})['general']['clean_mode'] == 'on':
        bot.delete_message(message.chat.id, message.message_id)
    markupjoin = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("ᴊᴏɪɴ ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ", url="https://t.me/+_FoaeZ-tvIQ4OGE9"), InlineKeyboardButton("ᴊᴏɪɴ ᴏꜰꜰɪᴄɪᴀʟ ᴄʜᴀɴɴᴇʟ", url="https://t.me/mortylab"))
    bot.send_message(message.chat.id, "Get support from here", reply_markup=markupjoin)






# /PLAY COMMAND
@bot.message_handler(commands=['play', 'play@morty_ai_bot'], chat_types=['private', 'group', 'supergroup'])
def play_command(message):
    chatID = message.chat.id
    if message.chat.type == 'group' or message.chat.type == 'supergroup':
        config_cleanmode = groups_collection.find_one({'id':str(chatID)})['general']['clean_mode']
        if config_cleanmode == 'on':
            try:
                bot.delete_message(chat_id=chatID, message_id=message.message_id)
            except telebot.apihelper.ApiTelegramException:
                bot.send_message(chatID, "I do not have enough admin rights. Give me admin privileges with `delete_messages` and `manage_chats` on.", parse_mode="Markdown")
                return   
            except:
                pass

    else:
        try:
            bot.delete_message(chat_id=chatID, message_id=message.message_id)
        except telebot.apihelper.ApiTelegramException:
            bot.send_message(chatID, "I do not have enough admin rights. Give me admin privileges with `delete_messages` and `manage_chats` on.", parse_mode="Markdown")
            return   
        except:
            pass

    
    
    if message.text == '/play@morty_ai_bot':
        query = message.text.replace('/play@morty_ai_bot','')
    else:
        query = message.text.replace('/play','')
    if len(query) == 0:
        bot.send_message(chatID, "Use in `/play songname` format\nExample:\n\n`/play intentions`", parse_mode="Markdown")
    else:
        if message.chat.type == 'group' or message.chat.type == 'supergroup':
            config_max = groups_collection.find_one({'id':str(chatID)})['play']['max_results']
        else:
            config_max = '10'
        query = query.strip()
        if 'movie' in query.lower() or 'cinema' in query.lower() or 'film' in query.lower() or 'full movie' in query.lower() or '2023' in query.lower():
            bot.send_message(chatID, "Stop trying to download movies bro...", parse_mode="Markdown")
        else:
            _message = bot.send_message(chatID, "⌛️", parse_mode='Markdown')
            dictdata = searchVideo(query, int(config_max))
            first_markup = InlineKeyboardMarkup()
            for title, urlsuffix in dictdata.items():
                urlwithhehe = 'hehe'+ urlsuffix
                first_markup.add(
                    InlineKeyboardButton(title, callback_data=urlwithhehe)
                )
            first_markup.add(
                InlineKeyboardButton("❌ Cancel ❌", callback_data="close")
            )
            bot.delete_message(message_id=_message.message_id, chat_id=chatID)
            bot.send_message(chat_id=chatID, text=f"<b>Found {str(len(dictdata))} results for {query} 🔎</b>\n\n👇", reply_markup=first_markup, parse_mode="html")





# CALLBACK QUERY HANDLERS FOR ALL COMMANDS WITH INLINEKEYBOARD CALLBACKS
@bot.callback_query_handler(func=lambda message: True)
def callback_query_handler(call):
    if call.data.startswith('hehe'):
        bot.answer_callback_query(call.id, 'Started downloading ✅', show_alert=False)
        if call.message.chat.type == 'private':
            subbed = isSubscriber(call.message.chat.id)
            if subbed == 0:
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
        else:
            now = datetime.datetime.now().timestamp()
            if call.message.chat.id in active_users:
                if time_difference(active_users[call.message.chat.id]):
                    active_users[call.message.chat.id] = now
                else:
                    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                    bot.send_message(chat_id=call.message.chat.id, parse_mode="Markdown", text="*ᴅᴏᴡɴʟᴏᴀᴅꜱ ᴀʀᴇ ʟɪᴍɪᴛᴇᴅ ᴛᴏ 1 ᴅᴏᴡɴʟᴏᴀᴅ ᴘᴇʀ 60 ꜱᴇᴄᴏɴᴅꜱ* (%dꜱ ʀᴇᴍᴀɪɴɪɴɢ)"%(60-(now - active_users[call.message.chat.id])))
                    return
            else:
                active_users[call.message.chat.id] = now

        def fn():
            limit = 2000000000
            if call.message.chat.type == 'private':
                if subbed == 1:
                    limit = 2000000000
                else:
                    limit = 1000000000
                    
            condition = call.message.chat.type == 'group' or call.message.chat.type == 'supergroup'
            private = call.message.chat.type == 'private'
            if condition:
                config_chataction = groups_collection.find_one({'id':str(call.message.chat.id)})['general']['chat_action']
                config_progressbar = groups_collection.find_one({'id':str(call.message.chat.id)})['general']['progress_animation']
            playurl = 'https://youtube.com'+call.data.replace('hehe','')
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            
            if condition and config_progressbar == 'on' or (private):
                _message = bot.send_message(chat_id=call.message.chat.id, text="Progress : ⬜⬛⬛⬛⬛⬛⬛⬛⬛")
            else:
                _message = bot.send_message(chat_id=call.message.chat.id, text='_Downloading . . ._', parse_mode='Markdown')
            
            html = requests.get(playurl).text
            if condition and config_progressbar == 'on' or (private):
                bot.edit_message_text(message_id=_message.message_id, chat_id=call.message.chat.id, text='Progress : ⬜⬜⬛⬛⬛⬛⬛⬛⬛')
            titleplay = re.findall(r"<title>(.*?)</title>", html)[0].replace("*", '').replace("_", '').replace("`", '').replace("[", '').strip()
            authorplay = re.findall(r"\"author\":\"(.*?)\"", html)[0].replace("*", '').replace("_", '').replace("`", '').replace("[", '').strip()
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
                                   'preferredquality':'192'}]
            }
            if condition and config_progressbar == 'on' or (private):
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=_message.message_id, text='Progress : ⬜⬜⬜⬛⬛⬛⬛⬛⬛')
            with YoutubeDL(ydl_opts) as ydl:
                try:
                    if condition and config_progressbar == 'on' or (private):
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=_message.message_id, text='Progress : ⬜⬜⬜⬜⬛⬛⬛⬛⬛')
                    ydl.download(playurl)
                    if condition and config_progressbar == 'on' or (private):
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=_message.message_id, text='Progress : ⬜⬜⬜⬜⬜⬛⬛⬛⬛')
                
                except Exception as e:
                    if 'country' in str(e):
                        bot.send_message(call.message.chat.id, "This video is not available on the BOT server's country")
                    else:
                        bot.edit_message_text(chat_id=_message.chat.id, message_id=_message.message_id, text="`❗️ ERROR WHILE DOWNLOADING`", parse_mode="Markdown")
                        towrite = {"URL":playurl, "Error":"ERROR WHILE DOWNLOADING MUSIC", "command":"/play", "Description":str(e)}
                        yterrorlogs_collection.insert_one(towrite)



            # PHASE 2        
            try:
                if condition and config_chataction == 'on':
                    bot.send_chat_action(chat_id=call.message.chat.id, action="upload_audio")
                if condition and config_progressbar == 'on' or (private):
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=_message.message_id, text='Progress : ⬜⬜⬜⬜⬜⬜⬛⬛⬛')
                filesize = os.path.getsize(filename+'.mp3') 
                if filesize >= limit:
                    bot.send_message(chat_id=call.message.chat.id, text=f"The filesize is too large ({filesize} bytes)! Subscribe to premium to increase filesize to 2GB!")
                    bot.delete_message(chat_id=_message.chat.id, message_id=_message.message_id)
                else:
                    if condition and config_progressbar == 'on' or (private):
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=_message.message_id, text='Progress : ⬜⬜⬜⬜⬜⬜⬜⬛⬛')
                    markupclose = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ", url=f"https://t.me/{BOT_USERNAME}?startgroup=start"), InlineKeyboardButton("❌ ᴄʟᴏꜱᴇ ᴘʟᴀʏᴇʀ ❌", callback_data="close"))
                    caption = f'{titleplay} | {authorplay}\n\n<b>Views</b> : {viewsplay}\n<b>Author</b> : {authorplay}\n<b>Published on</b> : {published_onplay}\n\n\n<a href="https://t.me/mortylab">Join MortyLabz</a> | <a href="https://buymeacoffee.com/mortylabz">Donate me</a>'
                    
                    file_uri = 'file://' + os.path.abspath(os.path.join(os.getcwd(), filename+'.mp3'))
                    if condition and config_progressbar == 'on' or (private):
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=_message.message_id, text='Progress : ⬜⬜⬜⬜⬜⬜⬜⬜⬛')
                    bot.send_audio(chat_id=call.message.chat.id,audio=file_uri, performer=authorplay, title=titleplay, caption=caption, parse_mode='html', reply_markup=markupclose)
                    bot.delete_message(chat_id=_message.chat.id, message_id=_message.message_id)

            except Exception as n:
                bot.edit_message_text(chat_id=_message.chat.id, message_id=_message.message_id, text="`❗️ ERROR WHILE SENTING`", parse_mode="Markdown")
                towrite2 = {"URL":playurl, "Error":"ERROR WHILE SENTING MUSIC", "command":"/play", "Description":str(n)}
                yterrorlogs_collection.insert_one(towrite2)

                
            #PHASE 3
            try:
                os.remove(filename+'.mp3')
            except:
                pass

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
        bot.answer_callback_query(call.id, 'Closed ✅', show_alert=False)

    elif call.data == 'video':
        markup = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("ᴜʟᴛʀᴀ ʜɪɢʜ ʀᴇꜱᴏʟᴜᴛɪᴏɴ", callback_data="privateultra"),InlineKeyboardButton("ʜɪɢʜ ʀᴇꜱᴏʟᴜᴛɪᴏɴ", callback_data="privatehigh"), InlineKeyboardButton("ʟᴏᴡ ʀᴇꜱᴏʟᴜᴛɪᴏɴ", callback_data="privatelow"), InlineKeyboardButton("﹤﹤ ʙᴀᴄᴋ", callback_data="home_yt"))
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)

    elif call.data == 'checkpremium':
        if isSubscriber(call.message.chat.id) == 1:
            submarkup = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Join soldier 💪", url="https://t.me/+HV8y_vKK99djZTBl"), InlineKeyboardButton("Cancel", callback_data="close"))
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=submarkup)
        else:
            dosubmarkup = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("👑 Subscribe 👑", url='https://buymeacoffee.com/mortylabz/e/122212'), InlineKeyboardButton("Cancel", callback_data="close"))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="*Subscribe to join our Men's premium gang with all the benefits 🗿☕️*",parse_mode="Markdown", reply_markup=dosubmarkup)
        
        
    elif call.data.startswith('private'):
        extension = None
        selection = None
        if call.data == 'privateultra':
            extension = '.mp4'
            selection = 'ultra high'
        elif call.data == 'privatehigh':
            extension = '.ogg'
            selection = 'high'
        elif call.data == 'privatelow':
            extension = '.mp4'
            selection = 'low'
        
        subbed = isSubscriber(call.message.chat.id)
        limit = 1000000000
        if subbed == 1:
            limit = 2000000000
        bot.answer_callback_query(call.id, 'Started downloading ✅', show_alert=False)
        if subbed == 0:
            now = datetime.datetime.now().timestamp()
            if call.message.chat.id in active_users:
                if time_difference(active_users[call.message.chat.id]):
                    active_users[call.message.chat.id] = now
                else:
                    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                    bot.send_message(chat_id=call.message.chat.id, parse_mode="Markdown", text="*Downloads are limited to 1 download per 60 seconds* (%ds remaining)\n\n/subscribe to get rid of rate limits :)"%(60-(now - active_users[call.message.chat.id])))
                    bot.delete_state(user_id=call.message.chat.id, chat_id=call.message.chat.id)
                    return
            else:
                active_users[call.message.chat.id] = now
        def fnhigh():
            if subbed == 0 and selection == 'ultra high':
                bot.delete_message(call.message.chat.id, call.message.message_id)
                bot.send_message(call.message.chat.id, "ᴜʟᴛʀᴀ ʜɪɢʜ ʀᴇꜱᴏʟᴜᴛɪᴏɴ ᴅᴏᴡɴʟᴏᴀᴅ ɪꜱ ᴏɴʟʏ ꜰᴏʀ ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀꜱ.\nꜱᴇɴᴅ /subscribe ᴛᴏ ʙᴇᴄᴏᴍᴇ ᴀ ᴘʀᴇᴍɪᴜᴍ ᴍᴇᴍʙᴇʀ.")
            else:
                with bot.retrieve_data(user_id=call.message.chat.id, chat_id=call.message.chat.id) as data:
                    youtubevideourl = data['yt_url']
                _message = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Progress : ⬜⬛⬛⬛⬛⬛⬛⬛⬛")
                filenamevideo = f'videogroup-{str(randomNumber())}'
                if selection == 'high':
                    ydl_optsvideo = {
                        "format":"bestvideo[ext=ogg]+bestaudio[ext=mp3]/best",
                        "outtmpl":filenamevideo+extension,
                        "geo_bypass":True,
                        "quiet":True,
                    }
                elif selection == 'low':
                    ydl_optsvideo = {
                        "format":"worstvideo[ext=mp4]+worstaudio[ext=m4a]/worst",
                        "outtmpl":filenamevideo+extension,
                        "geo_bypass":True,
                        "quiet":True,
                    }
                if selection == 'ultra high':
                    ydl_optsvideo = {
                        "format":"bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",
                        "outtmpl":filenamevideo+extension,
                        "geo_bypass":True,
                        "quiet":True,
                    }
                with YoutubeDL(ydl_optsvideo) as ydl:
                    bot.edit_message_text(chat_id=_message.chat.id, message_id=_message.message_id, text="Progress : ⬜⬜⬜⬛⬛⬛⬛⬛⬛")
                    try:
                        ydl.download(youtubevideourl) 
                        bot.edit_message_text(chat_id=_message.chat.id, message_id=_message.message_id, text="Progress : ⬜⬜⬜⬜⬜⬛⬛⬛⬛")              
                    except Exception as e:
                        if 'country' in str(e):
                            bot.send_message(call.message.chat.id, "This video is not available on the BOT server's country")
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="`❗️ Exception occured`", parse_mode="Markdown")
                        towrite = {"URL":youtubevideourl, "Error":f"ERROR WHILE DOWNLOADING {selection.upper()} RESOLUTION VIDEO", "command":"/youtube", "Description":str(e)}
                        yterrorlogs_collection.insert_one(towrite)
                    try:
                        bot.edit_message_text(chat_id=_message.chat.id, message_id=_message.message_id, text="Progress : ⬜⬜⬜⬜⬜⬜⬛⬛⬛")


                        file_size = os.path.getsize(filenamevideo+extension)

                        if file_size >= 1024**3:
                            file_size_cap = round(file_size / (1024**3), 2)
                            unit = "GB"
                        else:
                            file_size_cap = round(file_size / (1024**2), 2)
                            unit = "MB"


                        
                        if file_size >= limit:
                            bot.send_message(call.message.chat.id, f"Filesize is too large ({file_size_cap+unit})! Subscribe to premium to get unlimited filesize")
                            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

                    
                        else:
                            bot.edit_message_text(chat_id=_message.chat.id, message_id=_message.message_id, text="Progress : ⬜⬜⬜⬜⬜⬜⬜⬛⬛")
                            try:
                                html = requests.get(youtubevideourl).text
                                title = re.findall(r"<title>(.*?) - YouTube</title>", html)[0]
                            except:
                                title = 'Downloaded by Morty AI'
                            file_uri = 'file://' + os.path.abspath(os.path.join(os.getcwd(), filenamevideo+extension))
                            bot.send_chat_action(call.message.chat.id, action="upload_video")
                            bot.edit_message_text(chat_id=_message.chat.id, message_id=_message.message_id, text="Progress : ⬜⬜⬜⬜⬜⬜⬜⬜⬛")
                            bot.send_video(chat_id=call.message.chat.id, video=file_uri, caption=f"{title}\n\nQuality : <b>{selection.capitalize()} resolution ({str(file_size_cap)+unit})</b>\n\n\n<a href='https://t.me/mortylab'>Join MortyLabz</a> | <a href='https://buymeacoffee.com/mortylabz'>Donate me</a>", parse_mode="html", reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("Open in YouTube", url=f'{youtubevideourl}')))
                            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                    except Exception as q:
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="❗️ ERROR WHILE SENTING")
                        towrite2 = {"URL":youtubevideourl, "Error":f"ERROR WHILE SENTING {selection.upper()} RESOLUTION VIDEO", "command":"/youtube", "Description":str(q)}
                        yterrorlogs_collection.insert_one(towrite2)
                    try:
                        os.remove(filenamevideo+extension)
                    except:
                        pass

        threading.Thread(target=fnhigh).start()
        bot.delete_state(user_id=call.message.chat.id, chat_id=call.message.chat.id)
        





    elif call.data == 'audior':
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("ʜɪɢʜᴇꜱᴛ Qᴜᴀʟɪᴛʏ", callback_data="dwaud"), InlineKeyboardButton("﹤﹤ ʙᴀᴄᴋ", callback_data="home_yt")))


    elif call.data.startswith('hgroup'):
        selection = None
        extension = None
        if call.data == 'hgroupultra':
            selection = 'ultra high'
            extension = '.mp4'
        elif call.data == 'hgrouphigh':
            selection = 'high'
            extension = '.ogg'
        elif call.data == 'hgrouplow':
            selection = 'low'
            extension = '.mp4'
            
        
        with bot.retrieve_data(user_id=call.message.chat.id, chat_id=call.message.chat.id) as state:
            config_progressbar = state['config_progressbar']
            config_chataction = state['config_chataction']
            urlhigh = state['url']
 
        bot.answer_callback_query(call.id, 'Started downloading ✅', show_alert=False)
        now = datetime.datetime.now().timestamp()
        if call.message.from_user.id in active_users:
            if time_difference(active_users[call.message.from_user.id]):
                active_users[call.message.from_user.id] = now
            else:
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                bot.send_message(chat_id=call.message.chat.id, parse_mode="Markdown",disable_web_page_preview=True, text="*Downloads are limited to 1 download per 60 seconds* (%ds remaining)\n\n[Morty AI](https://t.me/morty_ai_bot)"%(60-(now - active_users[call.message.from_user.id])))
                bot.delete_state(chat_id=call.message.chat.id, user_id=call.message.chat.id)
                return
        else:
            active_users[call.message.from_user.id] = now

        def downloadhigh():
            if config_progressbar == 'on':
                _message = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Progress : ⬜⬛⬛⬛⬛⬛⬛⬛⬛")
            else:
                _message = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="`Downloading . . .`", parse_mode='Markdown')
            filenamevideogroup = f'videogroup-{str(randomNumber())}'
            if selection == "ultra high":
                ydl_optsvideo = {
                    "format":"bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",
                    "outtmpl":filenamevideogroup+'.mp4',
                    "geo_bypass":True,
                    "quiet":True,
                }
            elif selection == "high":
                ydl_optsvideo = {
                    "format":"bestvideo[ext=ogg]+bestaudio[ext=m4a]/best",
                    "outtmpl":filenamevideogroup+'.ogg',
                    "geo_bypass":True,
                    "quiet":True,
                }
            elif selection == 'low':
                ydl_optsvideo = {
                "format":"worstvideo[ext=mp4]+worstaudio[ext=m4a]/worst",
                "outtmpl":filenamevideogroup+'.mp4',
                "geo_bypass":True,
                "quiet":True,
            }
            
        

            if config_progressbar == 'on':
                bot.edit_message_text(chat_id=_message.chat.id, message_id=_message.message_id, text="Progress : ⬜⬜⬛⬛⬛⬛⬛⬛⬛")
            with YoutubeDL(ydl_optsvideo) as ydl:
                if config_progressbar == 'on':
                    bot.edit_message_text(chat_id=_message.chat.id, message_id=_message.message_id, text="Progress : ⬜⬜⬜⬛⬛⬛⬛⬛⬛")
                try:
                    ydl.download(urlhigh)
                    if config_progressbar == 'on':
                        bot.edit_message_text(chat_id=_message.chat.id, message_id=_message.message_id, text="Progress : ⬜⬜⬜⬜⬜⬛⬛⬛⬛")              
                except Exception as e:
                    if 'country' in str(e):
                        bot.send_message(call.message.chat.id, "This video is not available on the BOT server's country")
                    bot.edit_message_text(chat_id=_message.chat.id, message_id=_message.message_id, text="`❗️ Exception occured`", parse_mode="Markdown")
                    towrite = {"URL":urlhigh, "Error":"ERROR WHILE DOWNLOADING HIGH RESOLUTION VIDEO IN A GROUP", "command":"Youtube in group", "Description":str(e)}
                    yterrorlogs_collection.insert_one(towrite)


                try:
                    if config_progressbar == 'on':
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Progress : ⬜⬜⬜⬜⬜⬜⬛⬛⬛')
                    file_size = os.path.getsize(filenamevideogroup+extension)
                    if file_size >= 1024**3:
                        file_size_cap = round(file_size / (1024**3), 2)
                        unit = "GB"
                    else:
                        file_size_cap = round(file_size / (1024**2), 2)
                        unit = "MB"
                    if file_size>= 2000000000:
                        bot.edit_message_text(chat_id=call.message.chat.id,message_id=_message.message_id, text=f"`Filesize is above telegram's limitation so splitting the video into parts . . .`", parse_mode='Markdown')
                        file_dir = str(call.from_user.id).replace('-', '').strip()
                        files = split_video(filenamevideogroup+extension, file_dir)
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=_message.message_id, text=f'`Sending {len(files)} parts, total size is {str(file_size_cap)+unit} . . .`', parse_mode="Markdown")
                        part = 1
                        for i in files:
                            if config_chataction == 'on':
                                bot.send_chat_action(chat_id=call.message.chat.id, action="upload_video")
                            bot.send_video(chat_id=call.message.chat.id, video=i, caption=f"Quality : <b>{selection.capitalize()} resolution\n\nPart {part}/{len(files)}</b>\n\n\n<a href='https://t.me/mortylab'>Join MortyLabz</a> | <a href='https://buymeacoffee.com/mortylabz'>Donate me</a>", parse_mode="html", reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("Open in YouTube", url=f'{urlhigh}')))
                            part = part + 1 
                        bot.delete_message(chat_id=call.message.chat.id, message_id=_message.message_id)                     
                        shutil.rmtree(f'{str(call.from_user.id).replace("-", "").strip()}')


                    else:
                        if config_progressbar == 'on':
                            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Progress : ⬜⬜⬜⬜⬜⬜⬜⬛⬛')
                        try:
                            html = requests.get(urlhigh).text
                            title = re.findall(r"<title>(.*?) - YouTube</title>", html)[0]
                        except:
                            title = 'Downloaded by Morty AI'

                        file_uri = 'file://' + os.path.abspath(os.path.join(os.getcwd(), filenamevideogroup+extension))
                        if config_chataction == 'on':
                            bot.send_chat_action(call.message.chat.id, action="upload_video")
                        if config_progressbar == 'on':
                            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Progress : ⬜⬜⬜⬜⬜⬜⬜⬜⬛')
                        
                        bot.send_video(chat_id=call.message.chat.id, video=file_uri, caption=f"{title}\n\nQuality : <b>{selection.capitalize()} resolution ({str(file_size_cap)+unit})</b>\n\n\n<a href='https://t.me/mortylab'>Join MortyLabz</a> | <a href='https://buymeacoffee.com/mortylabz'>Donate me</a>", parse_mode="html", reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("Open in YouTube", url=f'{urlhigh}')))
                        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                            

                except Exception as q:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="❗️ ERROR WHILE SENTING")
                    towrite2 = {"URL":urlhigh, "Error":f"ERROR WHILE SENTING {selection.upper()} RESOLUTION VIDEO IN A GROUP", "command":"Youtube in group", "Description":str(q)}
                    yterrorlogs_collection.insert_one(towrite2)

                try:
                    os.remove(filenamevideogroup+extension)
                except:
                    pass

        threading.Thread(target=downloadhigh).start()
        bot.delete_state(user_id=call.message.chat.id, chat_id=call.message.chat.id)


    elif call.data == 'close_yt':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.delete_state(user_id=call.message.chat.id, chat_id=call.message.chat.id)
        




    elif call.data == 'home_yt':
        homemarkup = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton("ᴠɪᴅᴇᴏ 📹", callback_data="video"), InlineKeyboardButton("ᴀᴜᴅɪᴏ 🎧", callback_data="audior"), InlineKeyboardButton("❌ ᴄᴀɴᴄᴇʟ ❌", callback_data="close_yt"))
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=homemarkup)


    elif call.data.startswith('settings_'):
        admin_id = call.data.split('_')[1].strip()
        if call.from_user.id == int(admin_id):
            keyboards = [[InlineKeyboardButton('General', callback_data=f'gen_{call.from_user.id}'), InlineKeyboardButton('Image', callback_data=f'img_{call.from_user.id}'), InlineKeyboardButton('Play', callback_data=f'play_{call.from_user.id}')], [InlineKeyboardButton('❌ Close ❌', callback_data=f'cls_{call.from_user.id}')]]
            bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text=f'<b>Here is the settings Menu for {bot.get_chat(call.message.chat.id).title}</b>', reply_markup=InlineKeyboardMarkup(keyboard=keyboards), parse_mode='html')
        else:
            bot.answer_callback_query(call.id, "Only admins can perform this action", show_alert=True)





    elif call.data == 'dwaud':
        bot.answer_callback_query(call.id, 'Started downloading ✅', show_alert=False)
        subbed = isSubscriber(call.message.chat.id)
        if subbed == 0:
            now = datetime.datetime.now().timestamp()
            if call.message.chat.id in active_users:
                if time_difference(active_users[call.message.chat.id]):
                    active_users[call.message.chat.id] = now
                else:
                    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                    bot.send_message(chat_id=call.message.chat.id, parse_mode="Markdown", text="*Downloads are limited to 1 download per 60 seconds* (%ds remaining)\n\n/subscribe to get rid of rate limits :)"%(60-(now - active_users[call.message.chat.id])))
                    bot.delete_state(chat_id=call.message.chat.id, user_id=call.message.chat.id)
                    return
            else:
                active_users[call.message.chat.id] = now

        def fnaudio():
            chatID = call.message.chat.id
            limit = 1000000000
            if subbed == 1:
                limit = 2000000000
            with bot.retrieve_data(user_id=chatID, chat_id=chatID) as data:
                youtubevideourl = data['yt_url']
            filenameaudio = f'audiohigh-{str(randomNumber())}'
            _message = bot.edit_message_text(chat_id=chatID, message_id=call.message.message_id, text="Progress : ⬜⬛⬛⬛⬛⬛⬛⬛⬛")
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
                                   'preferredquality':'192'}]
            }
            bot.edit_message_text(chat_id=_message.chat.id, message_id=_message.message_id, text="Progress : ⬜⬜⬛⬛⬛⬛⬛⬛⬛")
            with YoutubeDL(ydl_opts) as ydl:
                bot.edit_message_text(chat_id=_message.chat.id, message_id=_message.message_id, text="Progress : ⬜⬜⬜⬛⬛⬛⬛⬛⬛")
                try:
                    ydl.download(youtubevideourl)
                    bot.edit_message_text(chat_id=_message.chat.id, message_id=_message.message_id, text="Progress : ⬜⬜⬜⬜⬜⬛⬛⬛⬛")
                except Exception as e:
                    if 'country' in str(e):
                        bot.send_message(chatID, "This video is not available on the BOT server's country")
                    bot.edit_message_text(chat_id=chatID, message_id=call.message.message_id, text="`❗️ Exception occured`", parse_mode="Markdown")
                    towrite = {"URL":youtubevideourl, "Error":"ERROR WHILE DOWNLOADING AUDIO", "command":"/youtube", "Description":str(e)}
                    yterrorlogs_collection.insert_one(towrite)

                try:
                    bot.edit_message_text(chat_id=_message.chat.id, message_id=_message.message_id, text="Progress : ⬜⬜⬜⬜⬜⬜⬛⬛⬛")
                    bot.send_chat_action(chat_id=chatID, action="upload_audio")
                    try:
                        html2 = requests.get(youtubevideourl).text
                        titleaudio = re.findall(r"<title>(.*?)</title>", html2)[0]
                    except:
                        titleaudio = 'Downloaded by Morty AI'

                    bot.edit_message_text(chat_id=chatID, message_id=call.message.message_id, text='Progress : ⬜⬜⬜⬜⬜⬜⬜⬛⬛')
                    if os.path.getsize(filenameaudio+'.mp3') >= limit:
                        bot.send_message(call.message.chat.id, "The filesize is too large! subscribe to increase filesize upto 2GB")
                    else:
                        caption = f'{titleaudio}\n\n\n<a href="https://t.me/mortylab">Join MortyLabz</a> | <a href="https://buymeacoffee.com/mortylabz">Donate me</a>'
                        file_uri = 'file://' + os.path.abspath(os.path.join(os.getcwd(), filenameaudio+'.mp3'))
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Progress : ⬜⬜⬜⬜⬜⬜⬜⬜⬛')
                        bot.send_audio(chat_id=chatID,audio=file_uri, caption=caption, parse_mode='html')
                        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                except Exception as n:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="❗️ ERROR WHILE SENTING")
                    towrite2 = {"URL":youtubevideourl, "Error":"ERROR WHILE SENTING AUDIO", "command":"/youtube", "Description":str(n)}
                    yterrorlogs_collection.insert_one(towrite2)

                try:
                    os.remove(filenameaudio+'.mp3')
                except:
                    pass

        threading.Thread(target=fnaudio).start()
        bot.delete_state(user_id=call.message.chat.id, chat_id=call.message.chat.id)


    elif call.data == 'usage':
        reply1 = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("﹤﹤ ʙᴀᴄᴋ", callback_data="acchom"))
        text = '━━━━━ ᴜꜱᴀɢᴇ ━━━━━\n\n★ 1 ɪᴍᴀɢᴇ = 2 ᴄʀᴇᴅɪᴛꜱ\n\n★ ɪꜰ ʏᴏᴜ ᴀʀᴇ ᴀ ꜱᴜʙꜱᴄʀɪʙᴇʀ 30 ᴄʀᴇᴅɪᴛꜱ ᴡɪʟʟ ʙᴇ ᴀᴅᴅᴇᴅ ᴛᴏ ʏᴏᴜʀ ᴀᴄᴄᴏᴜɴᴛ ᴅᴀɪʟʏ'
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=reply1)
    elif call.data == "acchom":
        markuppp = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton("ᴜꜱᴀɢᴇ", callback_data="usage"), InlineKeyboardButton("ᴄʟᴏꜱᴇ", callback_data="close"))
        msg = f'*━━━━━━ TOPUP ━━━━━━*\n\n*Topup from the list below, send the screenshot of proof* [here](https://t.me/ieatkidsforlunch) *for the redeem code.*\n\n*Use this code as* "`/topup Yourcode`" *to redeem your credits.*\n\nHere is the topup plans for credits:\n\n*1 ᴄʀᴇᴅɪᴛ              :   ₹29* ([ᴘᴀʏ ʜᴇʀᴇ](https://paytm.me/X-hCIVc))\n\n*3 Credits            :   ₹90* ([Pay here](https://paytm.me/oic-aio))\n\n*7 Credits            :   ₹210* ([Pay here](https://paytm.me/75-SJeJ))\n\n*16 Credits          :   ₹450* ([Pay here](https://paytm.me/9A9c-Ip))\n\n*30 Credits         :   ₹750* ([Pay here](https://paytm.me/DU9-cIp))\n\n*60 +5 Credits   :   ₹1450* ([Pay here](https://paytm.me/vr9-JeJ))'
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=msg, parse_mode="Markdown", disable_web_page_preview=True, reply_markup=markuppp)





    ############################## SETTINGS RELATED CALLBACK HANDLERS ##############################




    ############################## CLOSE MESSAGE (STARTS HERE) #############################
    elif call.data.startswith('cls_'):
        admin_id = call.data.replace('cls_', '').strip()
        if call.from_user.id == int(admin_id):
            bot.delete_state(user_id=int(admin_id), chat_id=call.message.chat.id)
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.answer_callback_query(call.id, 'Closed')
        else:
            bot.answer_callback_query(call.id, "Only admins can perform this action", show_alert=True)
    ############################## CLOSE MESSAGE (ENDS HERE) #############################





    ############################## SAVE CHANGES - CLEAN MODE(STARTS HERE) ##############################
    elif call.data.startswith('scln'):
        admin_id = call.data.split('_')[1].strip()
        if call.from_user.id == int(admin_id):
            
            if call.data.replace('scln', '').split('_')[0].strip() == 'off':
                cleanmode(chat_id=call.message.chat.id, action='on')
            elif call.data.replace('scln', '').split('_')[0].strip() == 'on':
                cleanmode(chat_id=call.message.chat.id, action='off')

            bot.delete_state(user_id=int(admin_id), chat_id=call.message.chat.id)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Changes saved ✅", reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton('<< Back', callback_data=f'cln_{admin_id}'),InlineKeyboardButton('❌ Close ❌', callback_data=f'cls_{admin_id}')))
            bot.answer_callback_query(call.id, text="Settings updated ✅")
        else:
            bot.answer_callback_query(call.id, "Only admins can perform this action", show_alert=True)
    ############################## SAVE CHANGES - CLEAN MODE (ENDS HERE) ##############################






    ############################## SAVE CHANGES - GET UPDATES (STARTS HERE) ##############################
    elif call.data.startswith('sgu'):
        admin_id = call.data.split('_')[1].strip()
        chatID = call.message.chat.id
        if call.from_user.id == int(admin_id):
            if call.data.replace('sgu', '').split('_')[0].strip() == 'on':
                get_updates(chat_id=chatID, action='on')
            elif call.data.replace('sgu', '').split('_')[0].strip() == 'off':
                get_updates(chat_id=chatID, action='off')


            bot.edit_message_text(chat_id=chatID, message_id=call.message.message_id, text="Changes saved ✅", reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton('<< Back', callback_data=f'gu_{admin_id}'), InlineKeyboardButton('❌ Close ❌', callback_data=f'cls_{admin_id}')))
            bot.answer_callback_query(call.id, text="Settings updated ✅")
        else:
            bot.answer_callback_query(call.id, "Only admins can perform this action", show_alert=True)
    ############################## SAVE CHANGES - GET UPDATES (ENDS HERE) ##############################






    ############################## SAVE CHANGES - NSFW FILTER (STARTS HERE) ##############################
    elif call.data.startswith('snsfw'):
        admin_id = call.data.split('_')[1].strip()
        chatID = call.message.chat.id
        if call.from_user.id == int(admin_id):
            
            if call.data.replace('snsfw', '').split('_')[0].strip() == 'off':
                nsfw(chat_id=chatID, action='on')
            elif call.data.replace('snsfw', '').split('_')[0].strip() == 'on':
                nsfw(chat_id=chatID, action='off')
            
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Changes saved ✅", reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("<< Back", callback_data=f'nsfw_{admin_id}'),InlineKeyboardButton('❌ Close ❌', callback_data=f'cls_{admin_id}')))
            bot.answer_callback_query(call.id, text="Settings updated ✅")
        else:
            bot.answer_callback_query(call.id, "Only admins can perform this action", show_alert=True)
    ############################## SAVE CHANGES - NSFW FILTER (ENDS HERE) ##############################









    ############################## SAVE CHANGES - YOUTUBE PROGRESSBAR (STARTS HERE) ############################## 
    elif call.data.startswith('sytpg'):
        admin_id = call.data.split('_')[1].strip()
        chatID = call.message.chat.id
        if call.from_user.id == int(admin_id):
            
            if call.data.replace('sytpg', '').split('_')[0].strip() == 'off':
                general_progress(chat_id=chatID, action='on')
            elif call.data.replace('sytpg', '').split('_')[0].strip() == 'on':
                general_progress(chat_id=chatID, action='off')
            

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=" Changes saved ✅", reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton('<< Back', callback_data=f'pg_{admin_id}'),InlineKeyboardButton('❌ Close ❌', callback_data=f'cls_{admin_id}')))
            bot.answer_callback_query(call.id, text="Settings updated ✅")
        else:
            bot.answer_callback_query(call.id, "Only admins can perform this action", show_alert=True)
    ############################## SAVE CHANGES - YOUTUBE PROGRESSBAR (ENDS HERE) ############################## 





    ############################## CHAT ACTION SAVE SETTINGS - MAIN (STARTS HERE) ##############################
    elif call.data.startswith('svact'):
        admin_id = call.data.split('_')[1].strip()
        chatID = call.message.chat.id
        if call.from_user.id == int(admin_id):
            
            if call.data.replace('svact', '').split('_')[0].strip() == 'off':
                chataction(chat_id=chatID, action='on')
            elif call.data.replace('svact', '').split('_')[0].strip() == 'on':
                chataction(chat_id=chatID, action='off')
            
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=" Changes saved ✅", reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton('<< Back', callback_data=f'chatact_{admin_id}'),InlineKeyboardButton('❌ Close ❌', callback_data=f'cls_{admin_id}')))
            bot.answer_callback_query(call.id, text="Settings updated ✅")
        else:
            bot.answer_callback_query(call.id, "Only admins can perform this action", show_alert=True)
    ############################## CHAT ACTION SAVE SETTINGS - MAIN (ENDS HERE) ##############################






    ############################## GENERAL SETTINGS - MAIN (STARTS HERE) ##############################
    elif call.data.startswith('gen_'):
        admin_id = call.data.replace('gen_', '').strip()
        chatID = call.message.chat.id
        group_name = bot.get_chat(chatID).title
        if call.from_user.id == int(admin_id):
            buttons = [[InlineKeyboardButton('Clean mode', callback_data=f'cln_{admin_id}'), InlineKeyboardButton('Get Updates', callback_data=f'gu_{admin_id}')], [InlineKeyboardButton('ProgressBar', callback_data=f'pg_{admin_id}'), InlineKeyboardButton('Chat action', callback_data=f'chatact_{admin_id}')],[InlineKeyboardButton("<< Back", callback_data=f"settings_{admin_id}")], [InlineKeyboardButton("❌ Close ❌", callback_data=f"cls_{admin_id}")]]
            bot.edit_message_text(chat_id=chatID,message_id=call.message.message_id, text=f'<b>General settings for {group_name}</b>\n\n<i>General settings contain all the settings for the basic functionality of the bot.</i>', reply_markup=InlineKeyboardMarkup(keyboard=buttons), parse_mode='html')
        else:
            bot.answer_callback_query(call.id, "Only admins can perform this action", show_alert=True)
    ############################## GENERAL SETTINGS - MAIN (ENDS HERE) #################################







    ############################# GET UPDATES SETTINGS - (STARTS HERE) #################################
    elif call.data.startswith('gu_'):
        admin_id = call.data.replace('gu_', '').strip()
        chatID = call.message.chat.id
        if call.from_user.id == int(admin_id):
            current_status_gu = groups_collection.find_one({'id':str(chatID)})['general']['get_updates']
            group_name_gu = bot.get_chat(chatID).title
            if current_status_gu == 'off':
                keys1 = [[InlineKeyboardButton('On', callback_data=f'onguoff_{admin_id}'), InlineKeyboardButton('Off', callback_data=f'ofguoff_{admin_id}')], [InlineKeyboardButton("<< Back", callback_data=f'gen_{admin_id}')], [InlineKeyboardButton('❌ Close ❌', callback_data=f'cls_{admin_id}')]]
                bot.edit_message_text(chat_id=chatID, message_id=call.message.message_id, text=f'<b>Get updates settings for {group_name_gu}</b>\n\n<i>If turned on, you will recieve feature updates, special offers, and other useful messages through the bot.</i>\n\n<b>Current status : Off</b> ❌', parse_mode='html', reply_markup=InlineKeyboardMarkup(keyboard=keys1))
            else:
                keys2 = [[InlineKeyboardButton('On', callback_data=f'onguon_{admin_id}'), InlineKeyboardButton('Off', callback_data=f'ofguon_{admin_id}')], [InlineKeyboardButton("<< Back", callback_data=f'gen_{admin_id}')], [InlineKeyboardButton('❌ Close ❌', callback_data=f'cls_{admin_id}')]]
                bot.edit_message_text(chat_id=chatID, message_id=call.message.message_id, text=f'<b>Get updates settings for {group_name_gu}</b>\n\n<i>If turned on, you will recieve feature updates, special offers, and other useful messages through the bot.</i>\n\n<b>Current status : On</b> ✅', parse_mode='html', reply_markup=InlineKeyboardMarkup(keyboard=keys2))
        else:
            bot.answer_callback_query(call.id, "Only admins can perform this action", show_alert=True)

    elif call.data.startswith('ofgu'):
        admin_id = call.data.split('_')[1].strip()
        chatID = call.message.chat.id
        if call.from_user.id == int(admin_id):
            current_status_gu = call.data.replace('ofgu', '').split('_')[0].strip()
            group_name_gu = bot.get_chat(chatID).title
            turn_off = current_status_gu
            if turn_off == 'on':
                bot.edit_message_text(chat_id=chatID, message_id=call.message.message_id, text='<b>Are you sure to turn off Get updates?</b>\n\nClick here to save changes', parse_mode='html', reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Save changes ✅", callback_data=f'sguoff_{admin_id}'), InlineKeyboardButton('<< Back', callback_data=f'gu_{admin_id}')))
            else:
                bot.answer_callback_query(call.id, text="Get updates is already off", show_alert=True)
        else:
            bot.answer_callback_query(call.id, "Only admins can perform this action", show_alert=True)

    elif call.data.startswith('ongu'):
        admin_id = call.data.split('_')[1].strip()
        chatID = call.message.chat.id
        if call.from_user.id == int(admin_id):
            
            group_name_gu = bot.get_chat(chatID).title
            current_status_gu = call.data.replace('ongu', '').split('_')[0].strip()
            turn_on = current_status_gu
            if turn_on == 'off':
                bot.edit_message_text(chat_id=chatID, message_id=call.message.message_id, text='<b>Are you sure to turn on Get updates?</b>\n\nClick here to save changes', parse_mode='html', reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Save changes ✅", callback_data=f'sguon_{admin_id}'), InlineKeyboardButton('<< Back', callback_data=f'gu_{admin_id}')))
            else:
                bot.answer_callback_query(call.id, text="Get updates is already on", show_alert=True)

        else:
            bot.answer_callback_query(call.id, "Only admins can perform this action", show_alert=True)
    ############################# GET UPDATES SETTINGS - (ENDS HERE) #################################









    ############################## CLEANMODE SETTINGS - MAIN (STARTS HERE) ##############################
    elif call.data.startswith('cln_'):
        chatID = call.message.chat.id
        admin_id = call.data.replace('cln_', '').strip()
        if call.from_user.id == int(admin_id):
            current_status = groups_collection.find_one({'id':str(chatID)})['general']['clean_mode']
            group_name = bot.get_chat(chatID).title
            if current_status == 'off':
                keys1 = [ [InlineKeyboardButton('On', callback_data=f'oncoff_{admin_id}'), InlineKeyboardButton("Off", callback_data=f'ofcoff_{admin_id}')], [InlineKeyboardButton('<< Back', callback_data=f'gen_{admin_id}')] , [InlineKeyboardButton('❌ Close ❌', callback_data=f'cls_{admin_id}')]] 
                markup_cleanmode1 = InlineKeyboardMarkup(keyboard=keys1)
                bot.edit_message_text(chat_id=chatID,message_id=call.message.message_id, text=f"<b>Clean mode settings for {group_name}</b>\n\n<i>If turned on, bot will delete the URL or query sent by users before replying. This brings a cleaner look to the bot's performance.</i>\n\n<b>Current status : Off</b> ❌", reply_markup=markup_cleanmode1, parse_mode='html')
            else:
                keys2 = [ [InlineKeyboardButton('On', callback_data=f'oncon_{admin_id}'), InlineKeyboardButton("Off", callback_data=f'ofcon_{admin_id}')], [InlineKeyboardButton('<< Back', callback_data=f'gen_{admin_id}')] , [InlineKeyboardButton('❌ Close ❌', callback_data=f'cls_{admin_id}')]]
                markup_cleanmode2 = InlineKeyboardMarkup(keyboard=keys2)
                bot.edit_message_text(chat_id=chatID,message_id=call.message.message_id, text=f"<b>Clean mode settings for {group_name}</b>\n\n<i>If turned on, bot will delete the URL or query sent by users before replying. This brings a cleaner look to the bot's performance.</i>\n\n<b>Current status : On</b> ✅", reply_markup=markup_cleanmode2, parse_mode='html')
        else:
            bot.answer_callback_query(call.id, "Only admins can do this action", show_alert=True)

    elif call.data.startswith('ofc'):
        chatID = call.message.chat.id
        admin_id = call.data.split('_')[1].strip()    
        current_status = call.data.replace('ofc', '').split('_')[0].strip()
        group_name = bot.get_chat(chatID).title
        if call.from_user.id == int(admin_id):
            turn_off = current_status
            if turn_off == 'on':
                bot.edit_message_text(chat_id=chatID, message_id=call.message.message_id, text='<b>Are you sure to turn off clean mode?</b>\n\nClick here to save changes', parse_mode='html', reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Save changes ✅", callback_data=f'sclnon_{admin_id}'), InlineKeyboardButton('<< Back', callback_data=f'cln_{admin_id}')))
            else:
                bot.answer_callback_query(call.id, text="Clean mode is already off", show_alert=True)
        else:
            bot.answer_callback_query(call.id, "Only admins can perform this action", show_alert=True)
    elif call.data.startswith('onc'):
        chatID = call.message.chat.id
        admin_id = call.data.split('_')[1].strip()
        current_status = call.data.replace('onc', '').split('_')[0].strip()
        if call.from_user.id == int(admin_id):
            turn_on = current_status
            if turn_on == 'off':
                bot.edit_message_text(chat_id=chatID, message_id=call.message.message_id, text='<b>Are you sure to turn on clean mode?</b>\n\nClick here to save changes', parse_mode='html', reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Save changes ✅", callback_data=f'sclnoff_{admin_id}'), InlineKeyboardButton('<< Back', callback_data=f'cln_{admin_id}')))
            else:
                bot.answer_callback_query(call.id, text="Clean mode is already on", show_alert=True)
        else:
            bot.answer_callback_query(call.id, "Only admins can perform this action", show_alert=True)
    ############################## CLEANMODE SETTINGS - MAIN (ENDS HERE) ##############################









    ############################## PROGRESSBAR SETTINGS - MAIN (STARTS HERE) ##############################
    elif call.data.startswith('pg_'):
        admin_id = call.data.replace('pg_', '').strip()
        chatID = call.message.chat.id
        if call.from_user.id == int(admin_id):
            group_name_youtube_pg = bot.get_chat(chatID).title
            current_status_youtube_pg = groups_collection.find_one({'id':str(chatID)})['general']['progress_animation']
            if current_status_youtube_pg == 'off':
                keys1 = [[InlineKeyboardButton('On', callback_data=f'onpgoff_{admin_id}'), InlineKeyboardButton('Off', callback_data=f'ofpgoff_{admin_id}')], [InlineKeyboardButton("<< Back", callback_data=f'gen_{admin_id}')], [InlineKeyboardButton('❌ Close ❌', callback_data=f'cls_{admin_id}')]]
                bot.edit_message_text(chat_id=chatID, message_id=call.message.message_id, text=f'<b>Download progressbar settings for {group_name_youtube_pg}</b>\n\n<i>If turned on, bot will have cool progressbar animation while downloading.</i>\n\n<b>Current status : Off</b> ❌', parse_mode='html', reply_markup=InlineKeyboardMarkup(keyboard=keys1))
            else:
                keys2 = [[InlineKeyboardButton('On', callback_data=f'onpgon_{admin_id}'), InlineKeyboardButton('Off', callback_data=f'ofpgon_{admin_id}')], [InlineKeyboardButton("<< Back", callback_data=f'gen_{admin_id}')], [InlineKeyboardButton('❌ Close ❌', callback_data=f'cls_{admin_id}')]]
                bot.edit_message_text(chat_id=chatID, message_id=call.message.message_id, text=f'<b>Download progressbar settings for {group_name_youtube_pg}</b>\n\n<i>If turned on, bot will have cool progressbar animation while downloading.</i>\n\n<b>Current status : On</b> ✅', parse_mode='html', reply_markup=InlineKeyboardMarkup(keyboard=keys2))
        else:
            bot.answer_callback_query(call.id, "Only admins can perform this action", show_alert=True)

    elif call.data.startswith('onpg'):
        admin_id = call.data.split('_')[1].strip()
        chatID = call.message.chat.id
        if call.from_user.id == int(admin_id):
            current_status_youtube_pg = call.data.replace('onpg', '').split('_')[0].strip()
            turn_on = current_status_youtube_pg
            if turn_on == 'off':
                bot.edit_message_text(chat_id=chatID, message_id=call.message.message_id, text='<b>Are you sure to turn on progressbar for Downloads?</b>\n\nClick here to save changes', parse_mode='html', reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Save changes ✅", callback_data=f'sytpgoff_{admin_id}'), InlineKeyboardButton('<< Back', callback_data=f'pg_{admin_id}')))
            else:
                bot.answer_callback_query(call.id, text="Download progressbar is already on", show_alert=True)
        else:
            bot.answer_callback_query(call.id, "Only admins can perform this action", show_alert=True)
    

    elif call.data.startswith('ofpg'):
        admin_id = call.data.split('_')[1].strip()
        chatID = call.message.chat.id
        if call.from_user.id == int(admin_id):
            current_status_youtube_pg = call.data.replace('ofpg', '').split('_')[0].strip()
            turn_off = current_status_youtube_pg
            if turn_off == 'on':
                bot.edit_message_text(chat_id=chatID, message_id=call.message.message_id, text='<b>Are you sure to turn off progressbar for Downloading?</b>\n\nClick here to save changes', parse_mode='html', reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Save changes ✅", callback_data=f'sytpgon_{admin_id}'), InlineKeyboardButton('<< Back', callback_data=f'pg_{admin_id}')))
            else:
                bot.answer_callback_query(call.id, text="Download progressbar is already off", show_alert=True)
        else:
            bot.answer_callback_query(call.id, "Only admins can perform this action", show_alert=True)
    ############################## PROGRESSBAR SETTINGS - MAIN (ENDS HERE) ##############################













    ############################## CHAT ACTION SETTINGS - MAIN (STARTS HERE) ##############################
    elif call.data.startswith('chatact_'):
        admin_id = call.data.replace('chatact_', '').strip()
        chatID = call.message.chat.id
        if call.from_user.id == int(admin_id):
            group_name_action = bot.get_chat(chatID).title
            current_status_action = groups_collection.find_one({'id':str(chatID)})['general']['chat_action']
        
            if current_status_action == 'off':
                keys1 = [[InlineKeyboardButton('On', callback_data=f'onactoff_{admin_id}'), InlineKeyboardButton('Off', callback_data=f'offactoff_{admin_id}')], [InlineKeyboardButton("<< Back", callback_data=f'gen_{admin_id}')], [InlineKeyboardButton('❌ Close ❌', callback_data=f'cls_{admin_id}')]]
                bot.edit_message_text(chat_id=chatID, message_id=call.message.message_id, text=f'<b>Chat action settings for {group_name_action}</b>\n\n<i>If turned on, bot will send chat action while senting the medias.</i>\n\n<b>Current status : Off</b> ❌', parse_mode='html', reply_markup=InlineKeyboardMarkup(keyboard=keys1))
            else:
                keys2 = [[InlineKeyboardButton('On', callback_data=f'onacton_{admin_id}'), InlineKeyboardButton('Off', callback_data=f'offacton_{admin_id}')], [InlineKeyboardButton("<< Back", callback_data=f'gen_{admin_id}')], [InlineKeyboardButton('❌ Close ❌', callback_data=f'cls_{admin_id}')]]
                bot.edit_message_text(chat_id=chatID, message_id=call.message.message_id, text=f'<b>Chat action settings for {group_name_action}</b>\n\n<i>If turned on, bot will send chat action while senting the medias.</i>\n\n<b>Current status : On</b> ✅', parse_mode='html', reply_markup=InlineKeyboardMarkup(keyboard=keys2))
        else:
            bot.answer_callback_query(call.id, "Only admins can perform this action", show_alert=True)
    
    
    elif call.data.startswith('onact'):
        admin_id = call.data.split('_')[1].strip()
        chatID = call.message.chat.id
        if call.from_user.id == int(admin_id):
            
            current_status_action = call.data.replace('onact', '').split('_')[0].strip()
            turn_on = current_status_action
            if turn_on == 'off':
                bot.edit_message_text(chat_id=chatID, message_id=call.message.message_id, text='<b>Are you sure to turn on chat action?</b>\n\nClick here to save changes', parse_mode='html', reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Save changes ✅", callback_data=f'svactoff_{admin_id}'), InlineKeyboardButton('<< Back', callback_data=f'chatact_{admin_id}')))
            else:
                bot.answer_callback_query(call.id, text="Chat action is already on", show_alert=True)
        else:
            bot.answer_callback_query(call.id, "Only admins can perform this action", show_alert=True)
    
    elif call.data.startswith('offact'):
        admin_id = call.data.split('_')[1].strip()
        chatID = call.message.chat.id
        if call.from_user.id == int(admin_id):
            current_status_action = call.data.replace('offact', '').split('_')[0].strip()
            turn_off = current_status_action
            if turn_off == 'on':
                bot.edit_message_text(chat_id=chatID, message_id=call.message.message_id, text='<b>Are you sure to turn off chat action?</b>\n\nClick here to save changes', parse_mode='html', reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Save changes ✅", callback_data=f'svacton_{admin_id}'), InlineKeyboardButton('<< Back', callback_data=f'chatact_{admin_id}')))
            else:
                bot.answer_callback_query(call.id, text="Chat action is already off", show_alert=True)
        else:
            bot.answer_callback_query(call.id, "Only admins can perform this action", show_alert=True)
    ############################## CHAT ACTION SETTINGS - MAIN (ENDS HERE) ##############################






    ############################## GENERAL SETTINGS - MAIN (ENDS HERE) ##############################








    ############################## PLAY SETTINGS - MAIN (STARTS HERE) ##############################
    elif call.data.startswith('play_'):
        admin_id = call.data.replace('play_', '').strip()
        chatID = call.message.chat.id
        group_name = bot.get_chat(chatID).title
        if call.from_user.id == int(admin_id):
            markup_play = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton('Max results', callback_data=f'max_{admin_id}'), InlineKeyboardButton("<< Back", callback_data=f"settings_{admin_id}"),InlineKeyboardButton("❌ Close ❌", callback_data=f"cls_{admin_id}"))
            bot.edit_message_text(chat_id=chatID,message_id=call.message.message_id, text=f'<b>Play settings for {group_name}</b>\n\n<i>These settings are related to the functionality of</i> <code>/play</code>', reply_markup=markup_play, parse_mode='html')
        else:
            bot.answer_callback_query(call.id, "Only admins can perform this action", show_alert=True)
    ############################## PLAY SETTINGS - MAIN (ENDS HERE) ##############################








    ############################## IMAGE SETTINGS - MAIN (STARTS HERE) ##############################
    elif call.data.startswith('img_'):
        admin_id = call.data.replace('img_', '').strip()
        chatID = call.message.chat.id
        group_name = bot.get_chat(chatID).title
        if call.from_user.id == int(admin_id):
            markup_image = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton('NSFW filter', callback_data=f'nsfw_{admin_id}'), InlineKeyboardButton("<< Back", callback_data=f"settings_{admin_id}"),InlineKeyboardButton("❌ Close ❌", callback_data=f"cls_{admin_id}"))
            bot.edit_message_text(chat_id=chatID,message_id=call.message.message_id, text=f'<b>Image settings for {group_name}</b>\n\n<i>These settings are related to the functionality of</i> <code>/img</code>', reply_markup=markup_image, parse_mode='html')
        else:
            bot.answer_callback_query(call.id, "Only admins can perform this action", show_alert=True)      



    elif call.data.startswith('nsfw_'):
        admin_id = call.data.replace('nsfw_', '').strip()
        chatID = call.message.chat.id
        if call.from_user.id == int(admin_id):
            group_name_nsfw = bot.get_chat(chatID).title
            current_status_nsfw = groups_collection.find_one({'id':str(chatID)})['image']['nsfw_filter']

            if current_status_nsfw == 'off':
                keys1  = [[InlineKeyboardButton('On', callback_data=f'onnsfwoff_{admin_id}'), InlineKeyboardButton('Off', callback_data=f'ofnsfwoff_{admin_id}')], [InlineKeyboardButton("<< Back", callback_data=f'img_{admin_id}')], [InlineKeyboardButton('❌ Close ❌', callback_data=f'cls_{admin_id}')]]
                bot.edit_message_text(chat_id=chatID, message_id=call.message.message_id, text=f'<b>NSFW filter settings for {group_name_nsfw}</b>\n\n<i>If turned on, bot will not produce NSFW images from user queries.</i>\n\n<b>Current status : Off</b> ❌', parse_mode='html', reply_markup=InlineKeyboardMarkup(keyboard=keys1))
            else:
                keys2 = [[InlineKeyboardButton('On', callback_data=f'onnsfwon_{admin_id}'), InlineKeyboardButton('Off', callback_data=f'ofnsfwon_{admin_id}')], [InlineKeyboardButton("<< Back", callback_data=f'img_{admin_id}')], [InlineKeyboardButton('❌ Close ❌', callback_data=f'cls_{admin_id}')]]
                bot.edit_message_text(chat_id=chatID, message_id=call.message.message_id, text=f'<b>NSFW filter settings for {group_name_nsfw}</b>\n\n<i>If turned on, bot will not produce NSFW images from user queries.</i>\n\n<b>Current status : On</b> ✅', parse_mode='html', reply_markup=InlineKeyboardMarkup(keyboard=keys2))
        else:
            bot.answer_callback_query(call.id, "Only admins can perform this action", show_alert=True)


    elif call.data.startswith('onnsfw'):
        admin_id = call.data.split('_')[1].strip()
        chatID = call.message.chat.id
        if call.from_user.id == int(admin_id):
            
            current_status_nsfw = call.data.replace('onnsfw', '').split('_')[0].strip()
            turn_on = current_status_nsfw
            if turn_on == 'off':
                bot.edit_message_text(chat_id=chatID, message_id=call.message.message_id, text='<b>Are you sure to turn on NSFW filtering?</b>\n\nClick here to save changes', parse_mode='html', reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Save changes ✅", callback_data=f'snsfwoff_{admin_id}'), InlineKeyboardButton('<< Back', callback_data=f'nsfw_{admin_id}')))
            else:
                bot.answer_callback_query(call.id, text="NSFW filtering is already on", show_alert=True)
        else:
            bot.answer_callback_query(call.id, "Only admins can perform this action", show_alert=True)
    elif call.data.startswith('ofnsfw'):
        admin_id = call.data.split('_')[1].strip()
        chatID = call.message.chat.id
        if call.from_user.id == int(admin_id):
            current_status_nsfw = call.data.replace('ofnsfw', '').split('_')[0].strip()
            turn_off = current_status_nsfw
            if turn_off == 'on':
                bot.edit_message_text(chat_id=chatID, message_id=call.message.message_id, text='<b>Are you sure to turn off NSFW filtering?</b>\n\nClick here to save changes', parse_mode='html', reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Save changes ✅", callback_data=f'snsfwon_{admin_id}'), InlineKeyboardButton('<< Back', callback_data=f'nsfw_{admin_id}')))
            else:
                bot.answer_callback_query(call.id, text="NSFW filtering is already off", show_alert=True)
        else:
            bot.answer_callback_query(call.id, "Only admins can perform this action", show_alert=True)
    ############################## IMAGE SETTINGS - MAIN (ENDS HERE) ##############################









    ############################## PLAY MAX RESULTS SETTINGS - SUB (STARTS HERE) ##############################
    elif call.data.startswith('max_'):
        admin_id = call.data.replace('max_', '').strip()
        chatID = call.message.chat.id
        if call.from_user.id == int(admin_id):
            group_name_max = bot.get_chat(chatID).title
            current_count = groups_collection.find_one({'id':str(chatID)})['play']['max_results']
            bot.edit_message_text(chat_id=chatID, message_id=call.message.message_id, text=f'<b>Max results settings for {group_name_max}</b>\n\n<i>This is the number of search results produced when you request a song using</i> <code>/play</code>.\n\n<b>Current count : {str(current_count).capitalize()}</b>\n\n\n<i>(NOTE: Click the below button, reply to the message within 10 seconds)</i>', parse_mode='html', reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Change count", callback_data=f'change{current_count}_{admin_id}'), InlineKeyboardButton('<< Back', callback_data=f'play_{admin_id}'),InlineKeyboardButton('❌ Close ❌', callback_data=f'cls_{admin_id}')))
        else:
            bot.answer_callback_query(call.id, "Only admins can perform this action", show_alert=True)







    elif call.data.startswith('change'):
        admin_id = call.data.split('_')[1].strip()
        chatID = call.message.chat.id
        if call.from_user.id == int(admin_id):
            
            current_count = int(call.data.replace('change', '').split('_')[0].strip())
            bot.edit_message_text(chat_id=chatID, message_id=call.message.message_id, text="Send me a new count between 1 - 10 👇\n\n<i>(Note: Reply within 10 seconds or you will need to perform it from the Beginning)</i>", parse_mode='html')
            bot.set_state(user_id=int(admin_id), chat_id=chatID, state=MyStates.maxcount)
            bot.add_data(user_id=int(admin_id), chat_id=chatID, admin_id=admin_id)
            def delete_state_function(user_id, chat_id):
                time.sleep(10)
                bot.delete_state(user_id=user_id, chat_id=chat_id)
            threading.Thread(target=delete_state_function, args=(int(admin_id), chatID)).start()
        else:
            bot.answer_callback_query(call.id, "Only admins can perform this action", show_alert=True)
    ############################## PLAY MAX RESULTS SETTINGS - SUB (ENDS HERE) ##############################
    elif call.data == 'request':
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text="Ok, What type of service are you trying to promote?", reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Bot", callback_data='promo_Bot'), InlineKeyboardButton("Channel", callback_data='promo_Channel'), InlineKeyboardButton("Other", callback_data='promo_Other')))
    elif call.data.startswith('promo'):
        promo_type = call.data.replace('promo_', '').strip()
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, f"Enter your product details below. Including the link, purpose and a short description 👇")
        bot.register_next_step_handler(message=call.message, callback=nextstep, promo_type=promo_type)

def nextstep(message, promo_type):
    request_to_send = f'Request by : @{message.from_user.username}\nUser ID : <code>{message.from_user.id}</code>\nFirst name : {message.from_user.first_name}\nType : {promo_type}\nTime : {datetime.datetime.now()}\nDescription : {message.text}'
    bot.send_message(int(SUDO_ID), request_to_send, parse_mode='html')
    bot.delete_message(message_id=message.message_id, chat_id=message.chat.id)
    bot.send_message(chat_id=message.chat.id,text="Your promotion request has been sent!\nYou will get a response within 24 hours")



@bot.message_handler(commands=['promorequest'], chat_types=['private'])
def request(message):
    bot.send_message(message.chat.id, f"MortyAI now have paid promotions, If you want to promote your bot/product/channel you can do it through our bot.\n\nIf you are planning for a promotion, you can send a promotion request here. We will get back to you once we review your request.", reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("Request promotion", callback_data='request')))




@bot.message_handler(state=MyStates.maxcount, is_digit=False)
def block_access(message):
    bot.send_message(chat_id=message.chat.id, reply_to_message_id=message.message_id, text='<i>Only supports digits ranging from 1 - 10</i>\n\nTry again to change the count', parse_mode='html')

@bot.message_handler(state=MyStates.maxcount, is_digit=True)
def set_new_count(message):
    chatID = message.chat.id
    message_id = message.message_id
    new_count = int(message.text)
    if new_count <= 0 or new_count >= 11:
        bot.send_message(chat_id=chatID, reply_to_message_id=message_id, text='<i>Only supports digits between 1 - 10.</i>\n\nTry again to change the count', parse_mode='html')
    else:
        groups_collection.update_one({'id':str(chatID)}, {'$set':{'play.max_results':new_count}})
        bot.delete_message(chatID, message_id)
        bot.send_message(chat_id=chatID, text=f'<b>Successfully set max results to {new_count}</b> ✅', parse_mode='html', reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("❌ Close ❌", callback_data=f'close')))
        bot.delete_state(user_id=message.from_user.id, chat_id=chatID)






bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())
bot.add_custom_filter(custom_filters.IsReplyFilter())






# /ACCOUNT COMMAND
@bot.message_handler(commands=['account'], chat_types=['private', 'group', 'supergroup'])
def account(message):
    bot.delete_message(message.chat.id, message.message_id)
    if message.chat.type == 'private':
        userID = message.chat.id
        firstname = message.chat.first_name
        lastname = message.chat.last_name
        username = message.chat.username
        bio = message.chat.bio
        
        
    elif message.chat.type == 'group' or message.chat.type == 'supergroup':
        userID = message.from_user.id
        firstname = message.from_user.first_name
        lastname = message.from_user.last_name
        username = message.from_user.username
        bio = "None"
        
    fetch = bot.send_message(message.chat.id, '⌛️')
    if collection_users.find_one({"id":str(userID)}):
        subscribed = 'No'
        if isSubscriber(userID) == 1:
            subscribed = 'Yes'
        p = collection_users.find_one({"id":str(userID)})
        total_credits = p['credits']
        joinedOn = datetime.datetime.fromtimestamp(p['joinedOn'])
        if lastname:
            name = firstname + " " + lastname
        else:
            name = firstname

        markup = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("ᴄʟᴏꜱᴇ", callback_data="close"))
        caption = f'━━━ {name} ━━━\n<b>╭━━━━━━━━━━━━━╮</b>\n<b>﹄ ᴜꜱᴇʀɴᴀᴍᴇ</b> : @{username}\n<b>﹄ ᴜꜱᴇʀ ɪᴅ</b> : {userID}\n<b>﹄ ᴄʀᴇᴅɪᴛꜱ</b> : <b>{total_credits}</b>\n<b>﹄ ɪꜱ ꜱᴜʙꜱᴄʀɪʙᴇʀ</b> : {subscribed}\n<b>﹄ ʙɪᴏ</b> : {bio}\n<b>﹄ ꜱᴛᴀʀᴛᴇᴅ ʙᴏᴛ ᴏɴ</b> : {str(joinedOn)[:10]}\n<b>╰━━━━━━━━━━━━━╯</b>'
        photos = bot.get_user_profile_photos(user_id=userID, limit=1)
        if len(photos.photos) >= 1:
            for i in photos.photos:
                bot.delete_message(chat_id=message.chat.id, message_id=fetch.message_id)
                bot.send_photo(chat_id=message.chat.id, photo=i[0].file_id, caption=caption, parse_mode="html", reply_markup=markup)
        else:
            bot.delete_message(chat_id=message.chat.id, message_id=fetch.message_id)
            bot.send_photo(chat_id=message.chat.id, photo='AgACAgUAAxkBAAEEPklkMb5hDEKzAAGwn7UJoPdJM_BFRlYAAqS3MRsLKIhVCDaNiU78a94BAAMCAANzAAMvBA', caption=caption, parse_mode='html', reply_markup=markup)
    else:
        if message.chat.type == 'private':
            bot.reply_to(message=message, text="You do not have an account yet.\nSend /start to create one.")
        else:
            bot.reply_to(message=message, text="You do not have an account yet.\nSend /start in my private message to create an account.")
        
    
    
    

@bot.message_handler(commands=['subscribe'], chat_types=['group', 'supergroup'])
def no(message):
    config_cleanmode = groups_collection.find_one({'id':str(message.chat.id)})['general']['clean_mode']
    if config_cleanmode == 'on':
        bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.chat.id, "ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ᴄᴀɴ ᴏɴʟʏ ʙᴇ ᴜꜱᴇᴅ ɪɴ ᴘʀɪᴠᴀᴛᴇ ᴍᴇꜱꜱᴀɢᴇꜱ")






# /SUBSCRIBE COMMAND
@bot.message_handler(commands=['subscribe'], chat_types=['private'])
def subscribe_command(message):
    notSubscribed = True
    accessCode = message.text.replace('/subscribe', '')
    accessCode = accessCode.strip()
    if len(accessCode) == 0:
        bot.send_message(message.chat.id, "*ᴛᴏᴅᴀʏ'ꜱ ᴏꜰꜰᴇʀ - ₹99* ([ᴘᴀʏ ʜᴇʀᴇ](https://paytm.me/C6C-akp))\n\n*ᴘʀᴇᴍɪᴜᴍ ɢᴀɴɢ* - *USD 10$* ([ᴘᴀʏ ʜᴇʀᴇ](https://buymeacoffee.com/mortylabz/e/122212))\n\nꜱᴇɴᴅ ᴛʜᴇ ᴘʀᴏᴏꜰ [ʜᴇʀᴇ](https://t.me/ieatkidsforlunch) ᴛᴏ ɢᴇᴛ ᴛʜᴇ ᴀᴄᴄᴇꜱꜱ ᴄᴏᴅᴇ.\n\nᴜꜱᴇ ᴛʜɪꜱ ᴀᴄᴄᴇꜱꜱ ᴄᴏᴅᴇ ᴀꜱ\n'`/subscribe Youraccesscode`'\nᴛᴏ ɢᴇᴛ ᴘʀᴇᴍɪᴜᴍ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ\n\nꜱᴇɴᴅ '`/subscribe status`' ᴛᴏ ꜱᴇᴇ ʏᴏᴜʀ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ ꜱᴛᴀᴛᴜꜱ.\n\nʏᴏᴜ ᴡɪʟʟ ɢᴇᴛ:\n✅ - *30 ᴄʀᴇᴅɪᴛꜱ ᴅᴀɪʟʏ*\n✅ - *ɴᴏ ʀᴀᴛᴇ ʟɪᴍɪᴛꜱ ꜰᴏʀ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ*\n✅ - *ɴᴏ ꜰɪʟᴇꜱɪᴢᴇ ʟɪᴍɪᴛ*\n✅ - *ᴡɪᴋɪ ʀᴇꜱᴜʟᴛ ʟɪɴᴇꜱ ᴜᴘᴛᴏ 10*\n✅ - *ᴜʟᴛʀᴀ ʀᴇᴀʟɪꜱᴛɪᴄ 4ᴋ ɪᴍᴀɢᴇꜱ*\n✅ - *3x ꜰᴀꜱᴛᴇʀ ᴅᴏᴡɴʟᴏᴀᴅ ꜱᴘᴇᴇᴅ*\n✅ - *ᴊᴏɪɴ ᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ ɢᴀɴɢ 🗿*\n✅ - *ᴀɴᴅ ᴍᴀɴʏ ᴍᴏʀᴇ*\n\n_(This is a lifetime subscription)_", parse_mode='Markdown', disable_web_page_preview=True)
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
            


# PROMOTE
@bot.message_handler(commands=['promote'])
def promotion_message(message):
    if message.chat.id == int(SUDO_ID):
        promotion_text = message.text.replace('/promote', '').strip()
        buttons = [[InlineKeyboardButton("❤️LOVE STATUS❤️", url='https://t.me/Prasadcreation1/3150')], [InlineKeyboardButton("🖤ALONE FEELING🖤", url='https://t.me/Prasadcreation1/3208')], [InlineKeyboardButton("😈ATTITUDE STATUS🤙", url='https://t.me/Prasadcreation1/3222')], [InlineKeyboardButton("💫TRENDING😍STATUS💫", url="https://t.me/Prasadcreation1/3202")], [InlineKeyboardButton("💔BROKEN STATUS💔", url="https://t.me/Prasadcreation1/3154")], [InlineKeyboardButton("😍RADHA KRISHNA😍", url='https://t.me/Prasadcreation1/3149')], [InlineKeyboardButton("☘️MAHADEV STATUS☘️", url="https://t.me/Prasadcreation1/3164")], [InlineKeyboardButton("💕LAYER STATUS💕", url='https://t.me/Prasadcreation1/3145')], [InlineKeyboardButton("💛BESTIE STATUS💜", url="https://t.me/Prasadcreation1/3034")], [InlineKeyboardButton('🧡JOIN OUR🧡 FAMILIY FRIENDS', url='https://t.me/Prasadcreation1')]]
        def promote(text, buttons,userID):
            to_send = []
            bot.send_message(int(userID), "Promotion message is now delivering. . .")
            bot.send_message(int(SUDO_ID), "Promotion message is now delivering. . .")
            for user in collection_users.find({}).sort([('_id', -1)]).limit(2500):
                to_send.append(user['id'])
            
            delay = 0.1

            for i in to_send:
                try:
                    bot.send_photo(chat_id=int(i), caption=text,photo='https://imgur.com/a/9w82CMo', reply_markup=InlineKeyboardMarkup(keyboard=buttons))
                    time.sleep(delay)              
                except Exception as e:
                    if '429' in str(e):
                        delay += 0.1
                        print(f"Ratelimit occured, increased to delay to {delay} seconds")
                        time.sleep(10)

            bot.send_message(int(userID), "Success! Your banner has been successfully sent to 2,500 users.")
            bot.send_message(int(SUDO_ID), "Promotion success")


        threading.Thread(target=promote, args=(promotion_text,buttons, 944359578)).start()
                



@bot.message_handler(commands=['verify'])
def verify(message):
    userid = message.chat.id
    with open('promoter.txt', 'a') as file:
        file.write(str(userid))

    bot.send_message(chat_id=message.chat.id, text="Verifiction successfull")



# /BC COMMAND (OWNER)
@bot.message_handler(commands=['bcprivate'], chat_types=['private'])
def bc_command(message):
    if str(message.chat.id) == SUDO_ID:
        query = message.text.replace('/bcprivate', '')
        if len(query) == 0:
            bot.send_message(int(SUDO_ID), "Type something")
        else:
            def broadcast_privates():
                bot.send_message(int(SUDO_ID), "Started delivering . . .")
                query = query.strip()
                removed_count = 0
                delay = 0.1
                limits = 0
                for i in collection_users.find({}):
                    try:
                        bot.send_message(int(i['id']), query, parse_mode='Markdown', disable_web_page_preview=True)
                        time.sleep(delay)
                    except Exception as e:
                        if '429' in str(e):
                            delay += 0.1
                            limits += 1
                            print(f"Ratelimit occured, increased to delay to {delay} seconds")
                            time.sleep(10)

                        if '403' in str(e):
                            collection_users.delete_one({'id':i['id']})
                            print(f"User blocked - Deleted {i['id']} from DB")
                            removed_count = removed_count + 1
            
                bot.send_message(int(SUDO_ID), f"Message sent successfull!\nRemoved {removed_count} users from DB.\n\nGot hit by Ratelimits {limits} times")
            threading.Thread(target=broadcast_privates).start()



@bot.message_handler(commands=['bcgroups'], chat_types=['private'])
def bc_groups(message):
    if str(message.chat.id) == SUDO_ID:
        query = message.text.replace('/bcgroups', '')
        if len(query) == 0:
            bot.send_message(int(SUDO_ID), "Type something")
        else:
            def broadcast_groups():
                bot.send_message(int(SUDO_ID), "Started delivering . . .")
                query = query.strip()
                removed_count = 0
                delay = 0.1
                limits = 0
                
                for i in groups_collection.find({}):
                    if i['general']['get_updates'] == 'on':
                        try:
                            bot.send_message(int(i['id']), query, parse_mode='Markdown', disable_web_page_preview=True)
                            time.sleep(delay)
                        except Exception as e:
                            if '429' in str(e):
                                delay += 0.1
                                limits += 1
                                print(f"Ratelimit occured, increased to delay to {delay} seconds")
                                time.sleep(10)

                            if '403' in str(e):
                                groups_collection.delete_one({'id':i['id']})
                                print(f"Blocked / No permission - Deleted group {i['id']} from DB")
                                removed_count = removed_count + 1


                bot.send_message(int(SUDO_ID), f"Message sent successfull!\nRemoved {removed_count} groups from DB.\n\nGot hit by {limits}")

            threading.Thread(target=broadcast_groups).start()






#/RESET COMMAND
@bot.message_handler(commands=['reset'], chat_types=['private'])
def reset_data(message):
    if str(message.chat.id) == SUDO_ID:
        res = resetFile()
        if res == "200":
            bot.send_message(int(SUDO_ID), "users collection has been resetted!")





@bot.message_handler(commands=['topup'], chat_types=['group', 'supergroup'])
def no(message):
    config_cleanmode = groups_collection.find_one({'id':str(message.chat.id)})['general']['clean_mode']
    if config_cleanmode == 'on':
        bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.chat.id, "ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ᴄᴀɴ ᴏɴʟʏ ʙᴇ ᴜꜱᴇᴅ ɪɴ ᴘʀɪᴠᴀᴛᴇ ᴍᴇꜱꜱᴀɢᴇꜱ")






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








# /IMG COMMAND
@bot.message_handler(commands=['img'], chat_types=['private', 'group', 'supergroup'])
def img_command(message):
    if message.chat.type == 'group' or message.chat.type == 'supergroup':
        config_cleanmode = groups_collection.find_one({'id':str(message.chat.id)})['general']['clean_mode']
        if config_cleanmode == 'on':
            bot.delete_message(message.chat.id, message.message_id)

    if message.text.startswith('/img'):
        if f'/img@{BOT_USERNAME}' in message.text:
            query = message.text.replace(f'/img@{BOT_USERNAME}', '').strip()
        else:
            query = message.text.replace('/img', '').strip()
    if len(query) == 0:
        bot.send_message(message.chat.id, "Use in '`/img query`' format\nExample :\n\n`/img Lion`\n\n*1 image = 2 credits*", parse_mode='Markdown')
    else:
        if message.chat.type == 'private':
            userID = message.chat.id
            if isSubscriber(userID) == 0:
                now = datetime.datetime.now().timestamp()
                if userID in active_users_wiki:
                    if time_difference_wiki(active_users_wiki[userID]):
                        active_users_wiki[userID] = now
                    else:
                        bot.send_message(chat_id=message.chat.id, parse_mode="Markdown", text="*ʀᴇQᴜᴇꜱᴛꜱ ᴀʀᴇ ʟɪᴍɪᴛᴇᴅ ᴛᴏ 1 ʀᴇQᴜᴇꜱᴛ ᴘᴇʀ 20 ꜱᴇᴄᴏɴᴅꜱ* (%dꜱ ʀᴇᴍᴀɪɴɪɴɢ)\n\n/subscribe ᴛᴏ ɢᴇᴛ ʀɪᴅ ᴏꜰ ʀᴀᴛᴇ ʟɪᴍɪᴛꜱ :)"%(20-(now - active_users_wiki[userID])))
                        return
                else:
                    active_users_wiki[userID] = now
        else:
            nsfw = groups_collection.find_one({'id':str(message.chat.id)})['image']['nsfw_filter']
            if nsfw == 'on':
                invalid_words = ['mommy','ejacu','toilet','ass','nood','without clothes','girl without','bare body','stab','cum','aunty','girlfriend','sister','handjob','licking','milf','hentai','donald','trump','sex','seduc','dwayne','clevage','girl wearing','fuk','pussy','horny','no clothes','suck','copulation','twerking','scarlett','fck','narendra','gangbang','intercourse','stepmom','stepsister','xxx','xnxx','whore','ass','hot girl','underwear','girl bathing','xi jingping','modi','brazzers','biden','joe','salman','porn','doggy','mia khalifa','sunny leone','bathing','hot girl','inner','inner wear','nanked','sexy','boob', 'leah gotti','nipple','kiss','fuck', 'dick', 'sex','asshole', 'vagina', 'naked','penis', 'butt','breast','chest','naced','abdomen','making out','tits','flirting','firting', 'nude', 'titty', 'titties','poop']
                for i in invalid_words:
                    if i in query.lower():
                        bot.send_message(chat_id=message.chat.id, text=FORBIDDEN, parse_mode='html')
                        return 'err'
            userID = message.from_user.id
            now = datetime.datetime.now().timestamp()
            if userID in active_users_wiki:
                if time_difference_wiki(active_users_wiki[userID]):
                    active_users_wiki[userID] = now
                else:
                    bot.send_message(chat_id=message.chat.id, parse_mode="Markdown",text="*ʀᴇQᴜᴇꜱᴛꜱ ᴀʀᴇ ʟɪᴍɪᴛᴇᴅ ᴛᴏ 1 ʀᴇQᴜᴇꜱᴛ ᴘᴇʀ 20 ꜱᴇᴄᴏɴᴅꜱ* (%dꜱ ʀᴇᴍᴀɪɴɪɴɢ)"%(20-(now - active_users_wiki[userID])))
                    return
            else:
                active_users_wiki[userID] = now


        user = collection_users.find_one({"id":str(userID)})
        if user:
            total_credits = user['credits']
            if total_credits <= 1:
                bot.send_message(chat_id=message.chat.id, parse_mode="Markdown",text=f"*Insufficent credits left on your account*\n\n*Credits needed : 2*\n*Credits left : {total_credits}*\n\nTopup some credits here /topup\nSubscribe to premium to get 30 credits daily (Lifetime)\nCheck account balance here /account")
            else:
                generate_image(query, message, total_credits, userID)
        else:
           bot.send_message(chat_id=message.chat.id,text="You do not have an account yet.\nSend /start in my private message to create an account.")
                
            





# /DEVELOPER COMMAND
@bot.message_handler(commands=['developer'])
def developer(message):
    if message.chat.type == 'group' or message.chat.type == 'supergroup':
        config_cleanmode = groups_collection.find_one({'id':str(message.chat.id)})['general']['clean_mode']
        if config_cleanmode == 'on':
            bot.delete_message(message.chat.id, message.message_id)
    keys = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Github", url="https://github.com/47hxl-53r"), InlineKeyboardButton("Telegram", url="https://t.me/mortylab"), InlineKeyboardButton("Buy me a coffee?", url="https://buymeacoffee.com/mortylabz"))
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
        if imgerrorlogs_collection.count_documents({}) == 0:
            errors.append("\nImg error logs are empty\n")
        else:
            for document in imgerrorlogs_collection.find({}):
                errors.append(f"--- IMG ERROR LOGS ---\n\nPROMPT : {document['PROMPT']}\nERROR : {document['ERROR']}\n\n")

        if igerrorlogs_collection.count_documents({}) == 0:
            errors.append("\nIg error logs are empty\n")
        else:
            for document in igerrorlogs_collection.find({}):
                errors.append(f"--- IG ERROR LOGS ---\n\nURL : {document['URL']}\nERROR : {document['ERROR']}\n\n")

        if yterrorlogs_collection.count_documents({}) == 0:
            errors.append("\nYt error logs are empty\n")
        else:
            for document1 in yterrorlogs_collection.find({}):
                errors.append(f"--- YT ERROR LOGS ---\n\nURL : {document1['URL']}\nERROR : {document1['Error']}\nCOMMAND : {document1['command']}\nDESCRIPTION : {document1['Description']}\n\n")
        
        for i in errors:
            with open('errors.txt', 'a') as f:
                f.write(i)
        with open('errors.txt', 'r') as f1:
            bot.send_document(chat_id=int(SUDO_ID), document=f1)
        bot.send_message(int(SUDO_ID), "Send /clearerrors to clear error logs")
        os.remove('errors.txt')

        




# /CLEARERRORS COMMAND
@bot.message_handler(commands=['clearerrors'], chat_types=['private'])
def clearerrors_command(message):
    if str(message.chat.id) == SUDO_ID:
        yterrorlogs_collection.delete_many({})
        imgerrorlogs_collection.delete_many({})
        igerrorlogs_collection.delete_many({})
        bot.send_message(message.chat.id, "Error Logs cleared")





@bot.message_handler(commands=['yt', 'ig', 'fb'], chat_types=['group', 'supergroup'])
def no(message):
    config_cleanmode = groups_collection.find_one({'id':str(message.chat.id)})['general']['clean_mode']
    if config_cleanmode == 'on':
        bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.chat.id, "ɪɴ ɢʀᴏᴜᴘꜱ ʏᴏᴜ ᴄᴀɴ ꜱɪᴍᴘʟʏ ᴊᴜꜱᴛ ꜱᴇɴᴛ ᴛʜᴇ ᴠɪᴅᴇᴏ ᴜʀʟ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ.")






# /YT COMMAND
@bot.message_handler(commands=['yt'], chat_types=['private'])
def youtube_command(message):
    query = message.text.replace('/yt', '', 1).strip()
    if len(query) == 0:
        bot.send_message(message.chat.id, "Use in `/yt url` format\nExample:\n\n`/yt https://youtu.be/dQw4w9WgXcQ`", parse_mode="Markdown")
    else:
        youtubevideourl = query
        if isValid(youtubevideourl):
            try:
                title = re.findall(r"<title>(.*?) - YouTube</title>", requests.get(youtubevideourl).text)[0]
            except:
                title = "NULL"
            
            bot.set_state(user_id=message.chat.id, chat_id=message.chat.id, state=MyStates.youtube)
            bot.add_data(user_id=message.chat.id, chat_id=message.chat.id, yt_url=youtubevideourl)
            markup = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton("ᴠɪᴅᴇᴏ 📹", callback_data= "video"), InlineKeyboardButton("ᴀᴜᴅɪᴏ 🎧", callback_data="audior"), InlineKeyboardButton("❌ ᴄᴀɴᴄᴇʟ ❌", callback_data="close_yt"))
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(chat_id=message.chat.id,text=f"<b>{title}</b>\n\n<b>Select an operation 👇</b>", reply_markup=markup, parse_mode="html", disable_web_page_preview=True)
        else:
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(message.chat.id, "Invalid URL detected")
            bot.delete_state(user_id=message.chat.id, chat_id=message.chat.id)








# /SCRAPE COMMAND
@bot.message_handler(commands=['scrape'], chat_types=['private', 'group', 'supergroup'])
def geturl(message):
    if message.chat.type == 'group' or message.chat.type == 'supergroup':
        config_cleanmode = groups_collection.find_one({'id':str(message.chat.id)})['general']['clean_mode']
        if config_cleanmode == 'on':
            bot.delete_message(message.chat.id, message.message_id)
    

    if f'/scrape@{BOT_USERNAME}' in message.text:
        url = message.text.replace(f'/scrape@{BOT_USERNAME}', '').strip()
    else:
        url = message.text.replace('/scrape', '').strip()

    if len(url) == 0:
        bot.send_message(message.chat.id,text="Send in `/scrape url` format (Including http:// or https://)\n\nExample:\n\n`/scrape https://google.com`", parse_mode="Markdown")
    else:
        if url.startswith('http://') or url.startswith('https://'):
            source_code = sourcecode(url)
            if source_code == 'err':
                bot.send_message(chat_id=message.chat.id, text="❗️ The given URL does not respond")
            elif source_code == 'timeout':
                bot.send_message(chat_id=message.chat.id, text= '❗️ Timeout occured! Site responding too slow!')
            else:
                if message.chat.type == 'group' or message.chat.type == 'supergroup':
                    if groups_collection.find_one({'id':str(message.chat.id)})['general']['chat_action'] == 'on':
                        bot.send_chat_action(chat_id=message.chat.id, action="upload_document")
                else:
                    bot.send_chat_action(chat_id=message.chat.id, action="upload_document")
                filename = f'scraped-{randomNumber()}.txt'
                try:
                    with open(filename, 'w+', encoding="utf-8") as f:
                        f.writelines(source_code)
                    file_uri = 'file://' + os.path.abspath(os.path.join(os.getcwd(), filename))
                    bot.send_document(chat_id=message.chat.id, document=file_uri, caption=f'\n\n[Join MortyLabz](https://t.me/mortylab) | [Donate me](https://buymeacoffee.com/mortylabz)', parse_mode="Markdown")

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
    config_cleanmode = groups_collection.find_one({'id':str(message.chat.id)})['general']['clean_mode']
    if config_cleanmode == 'on':
        bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.chat.id, "ꜱᴇɴᴅ ᴍᴇ ᴀɴʏ ʟɪɴᴋ ᴛᴏ ʏᴏᴜᴛᴜʙᴇ, ɪɴꜱᴛᴀɢʀᴀᴍ, ꜰᴀᴄᴇʙᴏᴏᴋ ᴍᴇᴅɪᴀꜱ ᴀɴᴅ ɪ ᴡɪʟʟ ᴅᴏᴡɴʟᴏᴀᴅ ɪᴛ ꜰᴏʀ ʏᴏᴜ.")

@bot.message_handler(content_types=['text'], chat_types=['group', 'supergroup'], text_startswith=('https://youtu.be', 'https://www.youtube.com', 'https://youtube.com','https://m.youtube.com'))
def reply(message):
    clean_mode = groups_collection.find_one({'id':str(message.chat.id)})['general']['clean_mode']
    if clean_mode == 'on': 
        try:
            bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        except:
            pass

    
    bot.set_state(user_id=message.chat.id, chat_id=message.chat.id, state=MyStates.youtube)
    url = message.text
    bot.add_data(user_id=message.chat.id, chat_id=message.chat.id, url=url)
    markup = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("ᴜʟᴛʀᴀ ʀᴇꜱᴏʟᴜᴛɪᴏɴ", callback_data=f"hgroupultra"),InlineKeyboardButton("ʜɪɢʜ ʀᴇꜱᴏʟᴜᴛɪᴏɴ", callback_data=f'hgrouphigh'), InlineKeyboardButton("ʟᴏᴡ ʀᴇꜱᴏʟᴜᴛɪᴏɴ", callback_data=f'hgrouplow'), InlineKeyboardButton("❌ ᴄʟᴏꜱᴇ ❌", callback_data="close_yt"))  
    bot.send_message(message.chat.id, f"*Hey @{message.from_user.username}*\n*ꜱᴇʟᴇᴄᴛ ᴀɴ ᴏᴘᴇʀᴀᴛɪᴏɴ* 👇",parse_mode='Markdown', reply_markup=markup, disable_web_page_preview=True)
    config_progressbar = groups_collection.find_one({'id':str(message.chat.id)})['general']['progress_animation']
    config_cleanmode = groups_collection.find_one({'id':str(message.chat.id)})['general']['clean_mode']
    config_chataction = groups_collection.find_one({'id':str(message.chat.id)})['general']['chat_action']
    bot.add_data(user_id=message.chat.id, chat_id=message.chat.id, config_progressbar=config_progressbar, config_cleanmode=config_cleanmode, config_chataction=config_chataction)
    #WORK HERE

bot.add_custom_filter(custom_filters.TextStartsFilter())
bot.add_custom_filter(custom_filters.IsAdminFilter(bot=bot))
    
    
@bot.message_handler(commands=['wiki', 'wiki@morty_ai_bot'], chat_types=['private', 'group', 'supergroup'])
def wiki_command(message):
    if message.chat.type == 'group' or message.chat.type == 'supergroup':
        config_cleanmode = groups_collection.find_one({'id':str(message.chat.id)})['general']['clean_mode']
        if config_cleanmode == 'on':
            bot.delete_message(message.chat.id, message.message_id)

    if message.text.startswith('/wiki'):
        if f'/wiki@{BOT_USERNAME}' in message.text:
            query = message.text.replace(f'/wiki@{BOT_USERNAME}', '').strip()
        else:
            query = message.text.replace('/wiki', '').strip()

    if len(query) == 0:
        bot.send_message(chat_id=message.chat.id,text="Use in '`/wiki query : sentence count`' format.\nExample:\n\n`/wiki donald trump : 4`\n\nUse : and supply number of sentences needed, if not, it defaults to 3.", parse_mode='Markdown')
    else:
        if query.count(':') >= 2:
            bot.send_message(chat_id=message.chat.id,text="Invalid syntax for this command.")
        else:
            if message.chat.type == 'private':
                if isSubscriber(message.chat.id) == 0:
                    now = datetime.datetime.now().timestamp()
                    if message.chat.id in active_users_wiki:
                        if time_difference_wiki(active_users_wiki[message.chat.id]):
                            active_users_wiki[message.chat.id] = now
                        else:
                            bot.send_message(chat_id=message.chat.id, parse_mode="Markdown", text="*ʀᴇQᴜᴇꜱᴛꜱ ᴀʀᴇ ʟɪᴍɪᴛᴇᴅ ᴛᴏ 1 ʀᴇQᴜᴇꜱᴛ ᴘᴇʀ 20 ꜱᴇᴄᴏɴᴅꜱ* (%dꜱ ʀᴇᴍᴀɪɴɪɴɢ)\n\n/subscribe ᴛᴏ ɢᴇᴛ ʀɪᴅ ᴏꜰ ʀᴀᴛᴇ ʟɪᴍɪᴛꜱ :)"%(20-(now - active_users_wiki[message.chat.id])))
                            return
                    else:
                        active_users_wiki[message.chat.id] = now
            else:
                now = datetime.datetime.now().timestamp()
                if message.chat.id in active_users_wiki:
                    if time_difference_wiki(active_users_wiki[message.chat.id]):
                        active_users_wiki[message.chat.id] = now
                    else:
                        bot.send_message(chat_id=message.chat.id, parse_mode="Markdown", text="*ʀᴇQᴜᴇꜱᴛꜱ ᴀʀᴇ ʟɪᴍɪᴛᴇᴅ ᴛᴏ 1 ʀᴇQᴜᴇꜱᴛ ᴘᴇʀ 20 ꜱᴇᴄᴏɴᴅꜱ* (%dꜱ ʀᴇᴍᴀɪɴɪɴɢ)"%(20-(now - active_users_wiki[message.chat.id])))
                        return
                else:
                    active_users_wiki[message.chat.id] = now


            query = query.strip()
            full = query.split(':')
            query = full[0].strip()
            if not len(full) == 1:
                lines = full[1].strip()
            else:
                lines = "3"
            if message.chat.type == 'group' or message.chat.type == 'supergroup':
                chatID = message.from_user.id
            else:
                chatID = message.chat.id

            if int(lines) >= 8 and isSubscriber(chatID) == 0:
                bot.send_message(chat_id=message.chat.id,text='Maximum number of sentences is 7.\n/subscribe to extend it to 10')
            else:
                if int(lines) >=11:
                    bot.send_message(chat_id=message.chat.id,  text="Maximum number of sentences is 10.")
                else:           
                    try:
                        result = f'<b><u>{query.capitalize()}</u></b>\n\n'+wikipedia.summary(query, sentences=int(lines))
                    except PageError:
                        result = 'Page not found, Try making your query more specific.'
                    except DisambiguationError as e:
                        result = str(e) + '\n\n<b>These are all possibilites of your query. Be more specific.</b>'
                    bot.send_message(chat_id=message.chat.id, text=result+'\n\n<a href="https://t.me/mortylab">Join Mortylabz</a> | <a href="https://buymeacoffee.com/mortylabz">Donate me</a>', parse_mode='html', disable_web_page_preview=True)






@bot.message_handler(commands=['settings'], chat_types=['group', 'supergroup'], is_chat_admin=True)
def settings_command(message):
        group = groups_collection.find_one({'id':str(message.chat.id)})
        if group:
            if group['general']['clean_mode'] == 'on':
                bot.delete_message(message.chat.id, message.message_id)
            keyboards = [[InlineKeyboardButton('General', callback_data=f'gen_{message.from_user.id}'), InlineKeyboardButton('Image', callback_data=f'img_{message.from_user.id}'), InlineKeyboardButton('Play', callback_data=f'play_{message.from_user.id}')], [InlineKeyboardButton('❌ Close ❌', callback_data=f'cls_{message.from_user.id}')]]
            bot.send_message(message.chat.id, f'<b>Here is the settings Menu for {bot.get_chat(message.chat.id).title}</b>', reply_markup=InlineKeyboardMarkup(keyboard=keyboards), parse_mode='html')
        else:
            bot.send_message(message.chat.id, "Group was not found in out database")
        


@bot.message_handler(commands=['settings'], chat_types=['group', 'supergroup'], is_chat_admin=False)
def stop(message):
    bot.reply_to(message, "This command can only be used by admins")




@bot.message_handler(commands=['fb'], chat_types=['private'])
def fb_private(message):
    url = message.text.replace('/fb', '', 1).strip()
    userID = message.chat.id
    if len(url) == 0:
        bot.send_message(userID, 'ꜱᴇɴᴛ ɪɴ `/fb URL` ꜰᴏʀᴍᴀᴛ\n\nᴇxᴀᴍᴘʟᴇ:\n\n`/fb https://fb.watch/jKsa4YuL8F/`\n\nᴛʜɪꜱ ꜰᴇᴀᴛᴜʀᴇ ɪꜱ ɴᴏᴛ ꜱᴜᴘᴘᴏʀᴛᴇᴅ ᴡɪᴛʜ ꜱᴛᴏʀɪᴇꜱ ʏᴇᴛ.', parse_mode='Markdown')
    else:
        def private():
            if not isFbLink(url):
                bot.send_message(userID, "ɪɴᴠᴀʟɪᴅ ꜰᴀᴄᴇʙᴏᴏᴋ ʟɪɴᴋ ᴅᴇᴛᴇᴄᴛᴇᴅ")
            else:
                if isSubscriber(userID) == 0:
                    now = datetime.datetime.now().timestamp()
                    if userID in active_users:
                        if time_difference(active_users[userID]):
                            active_users[userID] = now
                        else:
                            bot.delete_message(chat_id=userID, message_id=message.message_id)
                            bot.send_message(chat_id=userID, parse_mode="Markdown", text="*ᴅᴏᴡɴʟᴏᴀᴅꜱ ᴀʀᴇ ʟɪᴍɪᴛᴇᴅ ᴛᴏ 1 ᴅᴏᴡɴʟᴏᴀᴅ ᴘᴇʀ 60 ꜱᴇᴄᴏɴᴅꜱ* (%dꜱ ʀᴇᴍᴀɪɴɪɴɢ)\n\n/subscribe ᴛᴏ ɢᴇᴛ ʀɪᴅ ᴏꜰ ʀᴀᴛᴇ ʟɪᴍɪᴛꜱ :)"%(60-(now - active_users[userID])))
                            return
                    else:
                        active_users[userID] = now

                if url.startswith('https://www.facebook.com/reel') or url.startswith('https://fb.watch') or url.startswith('https://facebook.com/reel'):
                    bot.delete_message(userID, message.message_id)
                    _message = bot.send_message(userID, "🔎")
                    ydl_optsvideo = {"quiet":True}
                    with YoutubeDL(ydl_optsvideo) as ydl:
                        try:
                            dict_info = ydl.extract_info(url=url, download=False)
                        except Exception as e:
                            towrite = {'URL':url, 'ERROR':str(e)}
                            igerrorlogs_collection.insert_one(towrite)
                            bot.send_message(message.chat.id, "Exception while fetching data")


                        title = dict_info.get('title')
                        for i in dict_info.get('formats'):
                            if i['format_id'] == 'hd':
                                bot.send_chat_action(userID, action='upload_video')
                                caption = f'{title}\n\n\n<a href="https://t.me/mortylab">Join MortyLabz</a> | <a href="https://buymeacoffee.com/mortylabz">Donate me</a>'
                                try:
                                    bot.send_video(userID, video=i['url'], caption=caption, parse_mode='html', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("Open in Facebook", url=url)))
                                except Exception as c:
                                    towrite = {'URL':url, 'ERROR':str(c)}
                                    igerrorlogs_collection.insert_one(towrite)
                                    bot.send_message(message.chat.id, "Exception while sending video private")
                                bot.delete_message(userID, _message.message_id)
        threading.Thread(target=private).start()               

                





@bot.message_handler(content_types=['text'], chat_types=['group', 'supergroup'], text_startswith=('https://fb.watch','https://www.facebook.com/reel', 'https://facebook.com/reel'))
def fb_group(message):
    chatID = message.chat.id
    group = groups_collection.find_one({'id':str(chatID)})
    if group['general']['clean_mode'] == 'on': 
        try:
            bot.delete_message(chat_id=chatID, message_id=message.message_id)
        except:
            pass
    
    now = datetime.datetime.now().timestamp()
    if message.from_user.id in active_users:
        if time_difference(active_users[message.from_user.id]):
            active_users[message.from_user.id] = now
        else:
            bot.send_message(chat_id=chatID, parse_mode="Markdown",disable_web_page_preview=True, text="*Downloads are limited to 1 download per 60 seconds* (%ds remaining)\n\n[Morty AI](https://t.me/morty_ai_bot)"%(60-(now - active_users[message.from_user.id])))
            return
    else:
        active_users[message.from_user.id] = now

    
    def download():
        _message = bot.send_message(chatID, text='🔎')
        url = message.text 
        config_chataction = group['general']['chat_action']
        ydl_optsvideo = {"quiet":True}
        with YoutubeDL(ydl_optsvideo) as ydl:
            try:
                dict_info = ydl.extract_info(url=url, download=False)
            except Exception as e:
                towrite = {'URL':url, 'ERROR':str(e)}
                igerrorlogs_collection.insert_one(towrite)
                bot.send_message(message.chat.id, "Exception while fetching data")

            title = dict_info.get('title')
            for i in dict_info.get('formats'):
                if i['format_id'] == 'hd':
                    if config_chataction == 'on':
                        bot.send_chat_action(chatID, action='upload_video')
                    caption = f'{title}\n\n\n<a href="https://t.me/mortylab">Join MortyLabz</a> | <a href="https://buymeacoffee.com/mortylabz">Donate me</a>'
                    try:
                        bot.send_video(chatID, video=i['url'], caption=caption, parse_mode='html', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("Open in Facebook", url=url)))
                    except Exception as c:
                        towrite = {'URL':url, 'ERROR':str(c)}
                        igerrorlogs_collection.insert_one(towrite)
                        bot.send_message(message.chat.id, "Exception while sending video")

                    bot.delete_message(chatID, _message.message_id)

    threading.Thread(target=download).start()






bot.infinity_polling()






