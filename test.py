__author__ = 'Chad Peterson'
__email__ = 'chapeter@cisco.com'

import config
import datetime
import requests
import json
import smtplib
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from spark import ROOM

token = config.token
auth = "Bearer %s" % token
room = config.roomid
ignorelist = config.ignorelist
yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).date()
today = datetime.datetime.now()
date = today
room = ROOM(auth, room)

print room.title
for user in room.users:
    print user