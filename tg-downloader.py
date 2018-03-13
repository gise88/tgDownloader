import os
import logging
import configparser

from telethon import TelegramClient
from telethon import utils
from telethon.tl.types import PeerUser, PeerChat

from tgDownloader import settings

logger = logging.getLogger(settings.BOT_NAME)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class TGDownloader(object):
    
    def __init__(self, api_id, api_hash, phone_number, admins, enabled_chats):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number
        self.admins_id = admins
        self.enabled_chats_id = enabled_chats
        
        self.client = TelegramClient(settings.TELETHON_SESSION_NAME, self.api_id, self.api_hash)
        self.client.start(phone=self.phone_number)

        # Getting information about yourself
        self.me = self.client.get_me()
        # print(self.me.stringify())

        # Getting all the dialogs (conversations you have open)
        self.client.get_dialogs()
        
        self.admins_entities = []
        for admin_id in self.admins_id:
            self.admins_entities.append(self.client.get_entity(PeerUser(admin_id)))

        # self.chats_entities = []
        # for chat_id in self.enabled_chats_id:
        #     self.chats_entities.append(self.client.get_entity(PeerChat(chat_id)))

        for admin in self.admins_entities:
            print(admin.stringify())
        

    def start_bot(self):
    
        # Sending a message (you can use 'me' or 'self' to message yourself)
        # self.client.send_message(admin0, 'Hello World from Telethon!')
    
        # Sending a file
        # self.client.send_file(admin0, 'test-data/photo.jpg')
    
        # Retrieving messages from a chat
        
        # telegram = self.client.get_entity(PeerUser(777000))
        #
        # for message in self.client.get_messages(telegram, limit=5):
        #     print(utils.get_display_name(message.sender), message.message)
    
        # Listing all the dialogs (conversations you have open)
        # for dialog in self.client.get_dialogs():
        #     print(utils.get_display_name(dialog.entity))
    
        # Downloading profile photos (default path is the working directory)
        # self.client.download_profile_photo(self.admins_entities[2])
    
        # Once you have a message with .media (if message.media)
        # you can download it using client.download_media():
        # messages = client.get_messages(admin0)
        # client.download_media(messages[0])
        pass


if __name__ == '__main__':
    try:
        with open(settings.SECRETS_PATH, 'r') as f:
            config = configparser.ConfigParser()
            config.read_file(f)

            admins = []
            enabled_chats = []

            api_id = int(config[settings.TELEGRAM_CATEGORY][settings.TELEGRAM_API_ID_KEY])
            api_hash = config[settings.TELEGRAM_CATEGORY][settings.TELEGRAM_API_HASH_KEY]
            phone_number = config[settings.TELEGRAM_CATEGORY][settings.TELEGRAM_PHONE_NUMBER_KEY]
            
            print('Api id:', api_id)
            print('Api hash:', api_hash)
            print('Phone number:', phone_number)

            for key in config[settings.ADMINS_CATEGORY]:
                admins.append(int(config[settings.ADMINS_CATEGORY][key]))

            print('Admins:', admins)
            
            for key in config[settings.ENABLED_CHATS_CATEGORY]:
                enabled_chats.append(int(config[settings.ENABLED_CHATS_CATEGORY][key]))

            print('Enabled chats:', enabled_chats)

            # for section in config.sections():
            #     for key in config[section]:
            #         print(section, key, config[section][key])
    
            bot = TGDownloader(api_id, api_hash, phone_number, admins, enabled_chats)
            bot.start_bot()
        
    except IOError as e:
        logger.error(e)
