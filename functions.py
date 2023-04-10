import time, requests, random, platform, psutil, subprocess
import os
from pymongo import MongoClient
import math
# from openai.error import RateLimitError, APIError
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
AI_API_KEY = os.getenv('AI_API_KEY')
ERROR500 = 'AI Model is facing a slight traffic at this moment, Please try again after 5 minute.'
FORBIDDEN = '<b>Query filtered by NSFW filtering system 🔎</b>\n\n<i>Your admin can turn this off from\n/settings -> Image -> NSFW Filter</i>'
cluster = MongoClient("mongodb+srv://tzvri75136:Atulrv2005@mortydb.t0mwlvs.mongodb.net/?retryWrites=true&w=majority")
db = cluster['mortydb']
subs_collection = db['subscribers']
collection_users = db['users']
collection_codes = db['Accesscodes']



def resetFile():
    subscribers = []
    collection_users.update_many({}, {'$set':{"credits":4}})
    dat = subs_collection.find({})
    for da in dat:
        subscribers.append(da['id'])
    for i in subscribers:
        collection_users.update_one({"id":str(i)}, {'$set':{"credits":30}})
    return '200'
    



def get_stats():
    ram = psutil.virtual_memory()
    ram_total = ram.total // (1024 ** 2)
    ram_used = ram.used // (1024 ** 2)
    ram_percent = ram.percent
    disk = psutil.disk_usage('/')
    disk_total = disk.total // (1024 ** 3)
    disk_used = disk.used // (1024 ** 3)
    disk_percent = disk.percent
    cpu_percent = psutil.cpu_percent(interval=1)
    
    message = f'''
⚙️ <b>ꜱᴇʀᴠᴇʀ ꜱᴛᴀᴛᴜꜱ</b> ⚙️

⚡️ <b>ᴍᴀᴄʜɪɴᴇ</b> ⚡️
☞ ɴᴀᴍᴇ : MortyLabz server
☞ ᴛʏᴘᴇ : {platform.machine()}

⚡️ <b>ᴏꜱ</b> ⚡️
☞ ᴏꜱ : {platform.system() + platform.version()}
☞ ʀᴇʟᴇᴀꜱᴇ : {platform.release()}

⚡️ <b>ʀᴀᴍ</b> ⚡️
☞ ᴛᴏᴛᴀʟ ʀᴀᴍ : {ram_total}MB
☞ ʀᴀᴍ ᴜꜱᴇᴅ : {ram_used}MB
☞ ᴜꜱᴀɢᴇ ᴘᴇʀᴄᴇɴᴛ : {ram_percent}%

⚡️ <b>ᴅɪꜱᴋ</b> ⚡️
☞ ᴛᴏᴛᴀʟ ᴅɪꜱᴋ : {disk_total}GB
☞ ᴅɪꜱᴋ ᴜꜱᴇᴅ : {disk_used}GB
☞ ᴜꜱᴀɢᴇ ᴘᴇʀᴄᴇɴᴛ : {disk_percent}%

⚡️ <b>ᴄᴘᴜ</b>⚡️
☞ ᴄᴘᴜ : {platform.processor()}

☞ ᴄᴘᴜ ᴄᴏʀᴇꜱ : {os.cpu_count()} ᴄᴏʀᴇꜱ
☞ ᴄᴘᴜ ᴜꜱᴇᴅ : {cpu_percent}%
'''
    return message

    
    




def isValid(link):
    if 'youtu.be' in link or 'youtube.com' in link:
        return True
    else:
        return False
    
def isIgLink(link):
    if link.startswith('https://'):
        if 'instagram.com' in link:
            return True
        else:
            return False
    else:
        return False
    

def isFbLink(link):
    if link.startswith('https://'):
        
        if 'fb.watch' in link:
            return True
        elif 'facebook.com' in link:
            return True
        else:
            return False
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
    return status
    

# def split_video(input_file, output_dir):
#     ffprobe_cmd = f'ffprobe -i "{input_file}" -show_entries format=duration -v quiet -of csv="p=0"'
#     duration = float(subprocess.check_output(ffprobe_cmd, shell=True))
#     max_file_size = 2 * (1024**3)
#     part_duration = max_file_size / (os.path.getsize(input_file) / duration)
#     os.makedirs(output_dir, exist_ok=True)
#     output_files = []
#     start_time = 0
#     end_time = part_duration
#     while end_time < duration:
#         output_file = os.path.join(output_dir, f'{input_file.split(".")[0]}_{len(output_files)+1}.mp4')
#         output_files.append(os.path.relpath(output_file))
#         ffmpeg_cmd = f'ffmpeg -y -nostdin -loglevel warning -hide_banner -i "{input_file}" -ss {start_time} -to {end_time} -c copy "{output_file}"'
#         subprocess.call(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, shell=True)
#         start_time = end_time
#         end_time += part_duration
#     output_file = os.path.join(output_dir, f'{input_file.split(".")[0]}_{len(output_files)+1}.mp4')
#     output_files.append(os.path.relpath(output_file))
#     ffmpeg_cmd = f'ffmpeg -y -nostdin -loglevel warning -hide_banner -i "{input_file}" -ss {start_time} -to {duration} -c copy "{output_file}"'
#     subprocess.call(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, shell=True)
#     os.remove(input_file)
#     return output_files




def split_video(filename, output_dir):
    duration_command = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {filename}'
    duration_process = subprocess.Popen(duration_command, shell=True, stdout=subprocess.PIPE)
    duration_process.wait()
    duration = duration_process.stdout.read().decode().strip()
    part_duration = int(round(float(duration)) / 2)
    split_command = f'python3 split.py -f {filename} -s {part_duration} -o {output_dir} --extra "-v quiet"'
    process = subprocess.Popen(split_command, shell=True)
    process.communicate()
    to_return = []
    files = os.listdir(output_dir)
    for file in files:
        file_uri = "file://" + os.path.abspath(os.path.join(output_dir, file))
        to_return.append(file_uri)
        
    return to_return



