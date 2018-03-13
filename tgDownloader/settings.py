#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os


BOT_NAME = 'tgDownloader'

TELETHON_SESSION_NAME = 'session_name'

TELEGRAM_CATEGORY = 'TELEGRAM'
TELEGRAM_API_ID_KEY = 'api_id'
TELEGRAM_API_HASH_KEY = 'api_hash'
TELEGRAM_PHONE_NUMBER_KEY = 'phone_number'
ADMINS_CATEGORY = 'ADMINS'
ENABLED_CHATS_CATEGORY = 'ENABLED_CHATS'

# repository github
URL_REPO_GITHUB = 'https://github.com/gise88/tgDownloader'


# in this folder will be created the sqlite databases and the output directory for the audio files
WORKING_DIRECTORY_ABS_PATH = os.path.abspath('.')
SECRETS_FILE_NAME = 'SECRETS.conf'


# paths
SECRETS_PATH = os.path.join(WORKING_DIRECTORY_ABS_PATH, SECRETS_FILE_NAME)
