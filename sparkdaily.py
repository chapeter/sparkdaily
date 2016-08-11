__author__ = 'Chad Peterson'
__email__ = 'chapeter@cisco.com'

import config
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from spark import ROOM
import iso8601
import datetime
import pytz
import tzlocal

token = config.token
auth = "Bearer %s" % token
room = config.roomid
ignorelist = config.ignorelist
yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).date()
today = datetime.datetime.now()
date = yesterday
sender = config.sender
server = config.server
server_port = config.server_port
room = ROOM(auth, room)





def getDisplayName(personId, users):
    for user in users:
        if user.personId == personId:
            return user.displayname
    return "userID not found"


def buildEmailBody(room):
    body = "Here is what you may have missed yesterday in %s, %s-%s-%s:\n" \
           % (room.title, date.month, date.day, date.year)
    local_timezone = tzlocal.get_localzone()

    for message in reversed(room.messages):
        utcmsgtime = message['created']
        utcmsgtime = iso8601.parse_date(utcmsgtime)
        localmsgtime = utcmsgtime.replace(tzinfo=pytz.utc).astimezone(local_timezone)
        timestamp = str(localmsgtime.hour) + ":" +str(localmsgtime.minute) + ":" + str(localmsgtime.second)
        displayname = getDisplayName(message['personId'], room.users)
        body = body + "%s - %s: %s \n" % (timestamp, displayname, message['text'])


    return body


def sendEmail(room):
    sender = config.sender
    server = config.server
    server_port = config.server_port

    ###Build list of user email addresses
    userarray = []
    for user in room.users:
        for email in user.emails:
            userarray.append(email)

    msg = MIMEMultipart()
    body = MIMEText(str(buildEmailBody(room)).strip())

    msg['Subject'] = "Daily Spark Summary for %s" % room.title
    msg['From'] = sender
    msg['To'] = ", ".join(userarray)
    msg.attach(body)

    #print msg

    smtpObj = smtplib.SMTP(server, server_port)
    smtpObj.sendmail(msg["From"], msg["To"].split(","), msg.as_string())

    return

if __name__ == "__main__":
    sendEmail(room)

