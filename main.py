import os
import time
import hashlib
import pyautogui
from PIL import Image
from io import BytesIO
from telegram import Bot
import asyncio

# Telegram bot token
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

# Function to send image to Telegram
async def send_image_to_telegram(image):
    bio = BytesIO()
    image.save(bio, format="PNG")
    bio.seek(0)
    await bot.send_photo(chat_id=CHAT_ID, photo=bio)

async def main():
    # Initialize previous screenshot
    previous_screenshot = None

    while True:
        # Take a screenshot
        current_screenshot = take_screenshot()

        # Compare with the previous screenshot
        if previous_screenshot is not None and images_are_different(previous_screenshot, current_screenshot):
            # If different, send the new screenshot to Telegram
            await send_image_to_telegram(current_screenshot)

        # Save the current screenshot for comparison in the next iteration
        previous_screenshot = current_screenshot

        # Sleep for 5 seconds before taking the next screenshot
        await asyncio.sleep(5)  # Adjust the interval as needed

# Run the asyncio loop
asyncio.run(main())
