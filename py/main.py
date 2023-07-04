from telethon import TelegramClient
from telethon.events import NewMessage
from telethon.tl.types import MessageEntityTextUrl, MessageEntityUrl
from asyncio import run, sleep, CancelledError
from utils import parse_url
# from datetime import datetime
# from logging import info, warning, error, getLogger, Formatter, DEBUG
# from logging.handlers import RotatingFileHandler


# Use your own values from my.telegram.org
api_id = 20340026
api_hash = "d1c2010562443ded33c1f4fa64f16bc4"
client = TelegramClient("telegram", api_id, api_hash)
amazon_affiliate_id = "dualwarez-21"
channels_id = [
    1315464303,
    1491489500,
    810184328,
    1714047949,
]  # channels id that we want to recieve msgs from
our_channel_id = -980741307  # our channel id where we want to forward msg


# listen for new message
@client.on(NewMessage(chats=channels_id, incoming=True, forwards=False))
async def handle_new_message(event):
    try:
        print("Recieved new message..")

        is_amazon_link = False

        for entity in event.message.entities:
            url = False

            if isinstance(entity, MessageEntityUrl):
                url = event.message.raw_text[
                    entity.offset : entity.offset + entity.length
                ]
            elif isinstance(entity, MessageEntityTextUrl):
                url = entity.url
            else:
                break

            if url:
                parsed_url = parse_url(url, amazon_affiliate_id)
                is_amazon_link = parsed_url["is_amazon_link"]

                if is_amazon_link:
                    message = event.message.text.replace(url, parsed_url["updated"])
                    event.message.text = message

        if is_amazon_link:
            print("Sending message...")
            await client.send_message(our_channel_id, event.message)
            print("Message send!")
        else:
            # warning("Cannot found amazon link.")
            print("Cannot found amazon link.")

    except Exception as exception:
        # error({"message": event.message, "event": event, "error": exception})
        print("message: ",event.message,"\n","event: ",event,"\n", "error: ",exception)
        print("Error occured! Check logs for more.")
        pass


# async def main(restart_time=3600):    
#     while True:

#         await client.start()
#         await client.run_until_disconnected()
#         if client.is_connected:
#             print("Connected!")

#         await sleep(restart_time)

#         await client.disconnect()
#         if client.disconnected:
#             print("Disconnected")
#             await sleep(1.0)


# try:
#     client.start()
#     client.run_until_disconnected()
#     # run(main())
# except (KeyboardInterrupt):
#     print("Keyboard Interrupted!")
#     pass

client.start()
client.run_until_disconnected()