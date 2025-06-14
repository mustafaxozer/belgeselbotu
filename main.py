from telethon import TelegramClient
import asyncio
import os
from PIL import Image
from telethon.tl.types import MessageMediaPhoto

api_id = 25585459
api_hash = '01bfeb393e9ec6b0a8c4f8e400fc19ad'
phone_number = '+17423784812'

source_channel = 'trtbelgesel'
target_channel = 'tarihtebuguntur'

client = TelegramClient('kendi_session', api_id, api_hash)

async def crop_and_send_photo(message):
    try:
        temp_path = await message.download_media(file='temp_image.jpg')
        if temp_path is None:
            print("Görsel indirilemedi.")
            return
        from PIL import Image
        img = Image.open(temp_path)
        width, height = img.size
        if height <= 10:
            print("Görsel çok küçük, kırpılamaz.")
            return
        cropped = img.crop((0, 0, width, height - 100))
        cropped_path = 'cropped_image.jpg'
        cropped.save(cropped_path)
        await client.send_file(target_channel, file=cropped_path, caption=message.text or '')
        os.remove(temp_path)
        os.remove(cropped_path)
    except Exception as e:
        print(f"Fotoğraf işleme hatası: {e}")

async def paylas(mesaj):
    try:
        if isinstance(mesaj.media, MessageMediaPhoto):
            await crop_and_send_photo(mesaj)
        elif mesaj.media:
            await client.send_file(target_channel, file=mesaj.media, caption=mesaj.text or '')
        elif mesaj.text:
            await client.send_message(target_channel, mesaj.text)
        else:
            print("Ne medya ne metin var, atlanıyor.")
    except Exception as e:
        print(f"Paylaşım hatası: {e}")

async def kontrol_et():
    last_id = 0
    while True:
        try:
            async for mesaj in client.iter_messages(source_channel, limit=1):
                if mesaj.id > last_id:
                    last_id = mesaj.id
                    await paylas(mesaj)
        except Exception as e:
            print(f"Hata oluştu: {e}")
        await asyncio.sleep(5)

async def main():
    await client.start(phone=phone_number)
    print("Bot başladı.")
    await kontrol_et()

client.loop.run_until_complete(main())
