from get_mockup_link import generate_image
import urllib.request
import os
import logging
from PIL import Image
from aiogram import Bot, Dispatcher
from aiogram.utils.executor import start_webhook
import asyncio
import aioschedule


TOKEN = os.getenv('BOT_TOKEN')
HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')

wh_host = f'https://{HEROKU_APP_NAME}.herokuapp.com'
wh_path = f'/webhook/{TOKEN}'
wh_url = f'{wh_host}{wh_path}'

user_data = {}
whapp_host = '0.0.0.0'
whapp_port = os.getenv('PORT', default=8000)

logging.basicConfig(level=logging.INFO)

bot = Bot(TOKEN)
dp = Dispatcher(bot)
channel_id = -1001800523213

device = 'iphone'


@dp.message_handler()
async def generate_mockup():
    global device
    url = generate_image(device)
    device = 'iphone' if device == 'macbook' else 'macbook'
    urllib.request.urlretrieve(
        url,
        "mockup.png")
    img = Image.open('mockup.png')
    avg_color = img.resize((1, 1)).getpixel((0, 0))
    new_img = Image.new('RGBA', img.size, avg_color)
    new_img.paste(img, (0, 0), img)
    new_img.save('mockup.png')
    await bot.send_photo(photo=open('mockup.png', 'rb'), chat_id=channel_id, caption='@rewallpapers1')
    await bot.send_document(chat_id=channel_id, document=open('wp.jpg', 'rb'), caption='@rewallpapers1')


async def scheduler():
    aioschedule.every().minute.do(generate_mockup)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(dp):
    await bot.set_webhook(wh_url, drop_pending_updates=True)
    asyncio.create_task(scheduler())


async def on_shutdown(dispatcher):
    logging.warning('turning off')
    await bot.delete_webhook()
    await dispatcher.storage.close()
    logging.warning('bye ;)')

if __name__ == "__main__":
    print(whapp_host, whapp_port)
    start_webhook(
        dispatcher=dp,
        webhook_path=wh_path,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=whapp_host,
        port=whapp_port
    )
