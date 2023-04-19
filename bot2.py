import telebot
import os, time
from pymongo import MongoClient
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv, find_dotenv
cluster = MongoClient('mongodb+srv://secondmailofatul:Atulrv2005@cluster0.3bvqkv8.mongodb.net/?retryWrites=true&w=majority')
users_collection = cluster['mz']['users']
added_collection = cluster['mz']['addedusers']
load_dotenv(find_dotenv())

API = os.getenv('TELE_API_KEY')
SUDO = os.getenv('SUDO_ID')
DEVELOPER = os.getenv('DEVELOPER_ID')
bot = telebot.TeleBot(API, threaded=True)




@bot.my_chat_member_handler()
def handle(msg: telebot.types.ChatMemberUpdated):
    update = msg.new_chat_member
    if update.status == 'kicked':
        users_collection.delete_one({'id':str(msg.chat.id)})



bot.set_my_commands(commands=[
    telebot.types.BotCommand(command="start", description="Start me"),
    telebot.types.BotCommand(command="broadcast", description="Broadcast a message to users"),
    telebot.types.BotCommand(command='users', description="See total number of users")
],scope=telebot.types.BotCommandScopeChat(chat_id=int(SUDO)))



bot.set_my_commands(commands=[
    telebot.types.BotCommand(command="start", description="Start me"),
    telebot.types.BotCommand(command='help', description='Get some help')
],scope=telebot.types.BotCommandScopeAllPrivateChats())



@bot.message_handler(commands=['migrate123'])
def mig(message):
    users = []
    delay = 0.1
    migrated = 0
    for user in users_collection.find({}):
        users.append(user['id'])

    for i in users:
        try:
            bot.send_chat_action(chat_id=int(i), action='upload_audio')
            time.sleep(delay)
        except Exception as e:
            if '403' in str(e).lower():
                users_collection.delete_one({'id':str(i)})
                added_collection.insert_one({'id':str(i)})
                print("Migrated")
                migrated+=1
            if '429' in str(e):
                delay+=0.1
                time.sleep(10)
    
    bot.send_message(message.chat.id, f"Migrate complete\nMigrated {migrated} users to new database")


    

        

@bot.message_handler(commands=['start'], chat_types=['private'])
def starter(message):
    userID = message.from_user.id
    startmsg = f'Hello <a href="https://t.me/{message.from_user.username}">{message.from_user.first_name}</a>\nI\'m an auto approve Admin Join Requests Bot. I can approve users in Groups/Channels.Add me to your chat and promote me to admin with add members permission.'
    bot.send_photo(chat_id=message.chat.id, photo='https://imgur.com/a/f6VCoK2',caption=startmsg, parse_mode='html', reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("📽𝐌𝐨𝐯𝐢𝐞 𝐠𝐫𝐨𝐮𝐩📽", url='https://t.me/AllMovies_Grp'), InlineKeyboardButton("🎬𝐌𝐨𝐯𝐢𝐞 𝐜𝐡𝐚𝐧𝐧𝐞𝐥🎬", url='https://t.me/MZ_MOVIEZZ')))
    if not users_collection.find_one({"id":str(userID)}):
        users_collection.insert_one({'id':str(userID)}) 





@bot.message_handler(commands=['users'], chat_types=['private'])
def count(message):
    if message.from_user.id == int(SUDO) or message.from_user.id == int(DEVELOPER):
        users_count = users_collection.count_documents({})
        added_count = added_collection.count_documents({})
        total = users_count + added_count
        bot.send_message(message.chat.id, f"Total users : {total}\nBot users : {users_count}\nGroup approved users : {added_count}")
        


@bot.chat_join_request_handler()
def add(message):
    bot.approve_chat_join_request(chat_id=message.chat.id, user_id=message.from_user.id)
    added_collection.insert_one({'id':str(message.from_user.id)})
    addedmsg = f'Hello <a href="https://t.me/{message.from_user.username}">{message.from_user.first_name}</a>\nYou Request To Join 🔥{bot.get_chat(message.chat.id).title}🔥 Was Approved.'
    bot.send_photo(photo='https://imgur.com/a/f6VCoK2',chat_id=message.from_user.id, caption=addedmsg, parse_mode='html', reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("📽𝐌𝐨𝐯𝐢𝐞 𝐠𝐫𝐨𝐮𝐩📽", url='https://t.me/AllMovies_Grp'), InlineKeyboardButton("🎬𝐌𝐨𝐯𝐢𝐞 𝐜𝐡𝐚𝐧𝐧𝐞𝐥🎬", url='https://t.me/MZ_MOVIEZZ')))




@bot.message_handler(commands=['broadcast'], chat_types=['private'])
def broadcast_msg(message):
    if message.from_user.id == int(SUDO):
        if message.reply_to_message:
            users = []
            success = 0
            failure = 0
            delay = 0.1
            for user in users_collection.find({}):
                users.append(user['id'])
            total = len(users)
            if message.reply_to_message.photo:
                media = message.reply_to_message.photo[-1].file_id
                caption = message.reply_to_message.caption or ''
                for i in users:
                    try:
                        bot.send_photo(chat_id=i, photo=media, caption=caption)
                        success+=1
                        time.sleep(delay)
                    except Exception as first:
                        if '429' in str(first):
                            delay+=0.1
                            time.sleep(10)
                        if '403' in str(first):
                            failure+=1
                        

            elif message.reply_to_message.video:
                media = message.reply_to_message.video.file_id
                caption = message.reply_to_message.caption or ''
                for j in users:
                    try:
                        bot.send_video(chat_id=j, video=media, caption=caption)
                        success+=1
                        time.sleep(delay)
                    except Exception as second:
                        if '429' in str(second):
                            delay+=0.1
                            time.sleep(10)
                        if '403' in str(second):
                            failure+=1
                      

            elif message.reply_to_message.document:
                media = message.reply_to_message.document.file_id
                caption = message.reply_to_message.caption or ''
                for k in users:
                    try:
                        bot.send_document(chat_id=k, data=media, caption=caption)
                        success+=1
                        time.sleep(delay)
                    except Exception as third:
                        if '429' in str(third):
                            delay+=0.1
                            time.sleep(10)
                        if '403' in str(third):
                            failure+=1
                        
                        
            else:
                message_text = message.reply_to_message.text
                for l in users:
                    try:
                        bot.send_message(chat_id=l, text=message_text)
                        success+=1
                        time.sleep(delay)
                    except Exception as fourth:
                        if '429' in str(fourth):
                            delay+=0.1
                            time.sleep(10)
                        if '403' in str(fourth):
                            failure+=1
                    


            bot.reply_to(message, f"Broadcast complete!\n\nTotal : {total}\nSuccess : {success}\nFailure : {failure}")
        else:
            bot.send_message(int(SUDO), "Reply to a message.")
                      

bot.infinity_polling()



