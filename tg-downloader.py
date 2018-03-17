#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import logging
import mimetypes
import configparser

from telethon import TelegramClient
from telethon.tl.types import PeerChat
from telethon.tl.types import PeerUser
from telethon.tl.types import UpdateNewMessage
from telethon.tl.types import MessageMediaDocument
from telethon.tl.types import DocumentAttributeAnimated
from telethon.tl.types import DocumentAttributeFilename
from telethon.tl.types import InputDocumentFileLocation

from tgDownloader import settings
from tgDownloader.utils import format_size


# logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(settings.BOT_NAME)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

mimetypes.init()


class TGDownloader(object):
    def __init__(self, api_id, api_hash,
                 phone_number, admins,
                 enabled_chats, output_path):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number
        self.admins_id = admins
        self.enabled_chats_id = enabled_chats
        self.output_path = output_path
        
        self.client = TelegramClient(
            settings.TELETHON_SESSION_NAME,
            self.api_id, self.api_hash,
            update_workers=1,
            spawn_read_thread=False
        )
        self.client.start(phone=self.phone_number)
        
        # Getting information about yourself
        self.me = self.client.get_me()
        # print(self.me.stringify())
        
        # Getting all the dialogs (conversations you have open)
        # !!! get_dialogs is MANDATORY !!!
        dialogs = self.client.get_dialogs()
        # for i, dialog in enumerate(dialogs, start=1):
        #     sprint('{:3d}. {} | {}'.format(
        #         i, get_display_name(dialog.entity), dialog.entity.id))
        
        self.admins_entities = { }
        for admin_id in self.admins_id:
            self.admins_entities[admin_id] = \
                self.client.get_entity(PeerUser(admin_id))
        
        self.chats_entities = []
        for chat_id in self.enabled_chats_id:
            self.chats_entities[chat_id] = \
                self.client.get_entity(PeerChat(chat_id))
        
        # for admin in self.admins_entities:
        #     print(admin.stringify())
    
    
    def progress_callback(self, file_name,
                          chat_entity, reply_message):
        def progress(size, total_size):
            self.client.edit_message(
                chat_entity,
                reply_message,
                'Name: {0}\n'
                '{1:0.2f}% of total\n'
                'Size: {2} / {3}'.format(
                    file_name,
                    (size / total_size) * 100.0,
                    format_size(size),
                    format_size(total_size)
                )
            )
        
        
        return progress
    
    
    def update_handler(self, update):
        if isinstance(update, UpdateNewMessage) and \
                not update.message.out and \
                update.message.media and \
                isinstance(update.message.media,
                           MessageMediaDocument):
            try:
                msg = update.message
                doc = msg.media.document
                is_video = (isinstance(doc.mime_type, str) and
                            doc.mime_type.startswith('video/'))
                is_gif = len(list(filter(
                    lambda x: isinstance(
                        x, DocumentAttributeAnimated),
                    doc.attributes))) > 0
                
                if is_video and not is_gif and \
                        (msg.from_id in self.admins_id or
                         (msg.fwd_from.from_id in self.admins_id
                         if msg.fwd_from else False)):
                    file_name = list(map(
                        lambda x: x.file_name,
                        filter(
                            lambda x:
                            isinstance(x, DocumentAttributeFilename),
                            doc.attributes)))
                    
                    file_name = file_name[0] if len(file_name) == 1 else \
                        '{0}{1}'.format(
                            doc.date.strftime('video_%Y-%m-%d_%H-%M-%S'),
                            mimetypes.guess_extension(doc.mime_type)
                        )
                    file_path = os.path.join(self.output_path, file_name)
                    
                    print('{0} requests {1}'.format(
                        file_name,
                        self.admins_entities[msg.from_id]).stringify()
                          )
                    
                    reply_message = self.client.send_message(
                        msg.to_id,
                        'Managing your request...',
                        reply_to=msg
                    )
                    
                    self.client.download_file(
                        InputDocumentFileLocation(
                            id=doc.id,
                            access_hash=doc.access_hash,
                            version=doc.version
                        ),
                        file_path,
                        file_size=doc.size,
                        progress_callback=self.progress_callback(
                            file_name,
                            msg.to_id,
                            reply_message
                        ),
                        part_size_kb=1024
                    )
            
            except Exception as e:
                print(e)
    
    
    def start_and_idle_bot(self):
        self.client.add_event_handler(self.update_handler)
        self.client.idle()


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
            output_path = config[settings.BOT_SETTINGS_CATEGORY][settings.DOWNLOAD_OUTPUT_PATH_KEY]
            
            print('Api id:', api_id)
            print('Api hash:', api_hash)
            print('Phone number:', phone_number)
            
            for key in config[settings.ADMINS_CATEGORY]:
                admins.append(
                    int(config[settings.ADMINS_CATEGORY][key]))
            
            print('Admins:', admins)
            
            for key in config[settings.ENABLED_CHATS_CATEGORY]:
                enabled_chats.append(
                    int(config[settings.ENABLED_CHATS_CATEGORY][key]))
            
            print('Enabled chats:', enabled_chats)
            
            bot = TGDownloader(
                api_id,
                api_hash,
                phone_number,
                admins,
                enabled_chats,
                output_path
            )
            bot.start_and_idle_bot()
    
    except IOError as e:
        logger.error(e)
