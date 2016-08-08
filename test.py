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
sender = config.sender
server = config.server
server_port = config.server_port
room = ROOM(auth, room)
print room.title

def buildEmail(room):
    sender = config.sender
    server = config.server
    server_port = config.server_port

    ###Build list of user email addresses
    userarray = []
    for user in room.users:
        userarray.append(user['email'])

    msg = MIMEMultipart()
    #body = MIMEText(str(createEmailBody(todayMessage(), room)).strip())

    msg['Subject'] = "Daily Spark Summary for %s" % room.title
    msg['From'] = sender
    msg['To'] = ", ".join(userarray)
    #msg.attach(body)

    print msg

    #smtpObj = smtplib.SMTP(server, server_port)
    #smtpObj.sendmail(msg["From"], msg["To"].split(","), msg.as_string())


buildEmail(room)
