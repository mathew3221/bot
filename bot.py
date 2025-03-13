import os
import random
import time
from moviepy.editor import VideoFileClip
from pyrogram import Client, filters
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_ID = os.getenv("28428963")
API_HASH = os.getenv("24a2d580293f545cf828a6a64104cbe9")
BOT_TOKEN = os.getenv("7501299734:AAGhvyOSmIp4aTMmqNBX-csmqHTFvCoLImw")

bot = Client("screenshot_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def extract_screenshots(video_path, output_folder, num_screenshots=5):
    clip = VideoFileClip(video_path)
    duration = clip.duration
    timestamps = sorted(random.sample(range(int(duration)), num_screenshots))
    
    os.makedirs(output_folder, exist_ok=True)
    screenshots = []
    
    for i, t in enumerate(timestamps):
        frame_path = os.path.join(output_folder, f"screenshot_{i+1}.jpg")
        clip.save_frame(frame_path, t)
        screenshots.append(frame_path)

    clip.close()
    return screenshots

@bot.on_message(filters.video)
def handle_video(client, message):
    video_path = f"downloads/{message.video.file_id}.mp4"
    output_folder = "screenshots"

    # Download the video
    message.download(video_path)
    
    # Generate a random number of screenshots (3-7)
    num_screenshots = random.randint(3, 7)
    screenshots = extract_screenshots(video_path, output_folder, num_screenshots)

    # Send screenshots back to the user
    for screenshot in screenshots:
        message.reply_photo(photo=screenshot)
    
    # Clean up
    os.remove(video_path)
    for screenshot in screenshots:
        os.remove(screenshot)

bot.run()
