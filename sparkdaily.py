__author__ = 'Chad Peterson'
__email__ = 'chapeter@cisco.com'

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from spark import ROOM
import iso8601
import datetime
import pytz
import tzlocal
import os

token = os.environ['SPARK_TOKEN']
room = os.environ['SPARK_ROOM']
auth = "Bearer %s" % token
room = ROOM(auth, room)





def getDisplayName(personId, users):
    for user in users:
        if user.personId == personId:
            return user.displayname
    return "userID not found"


def msgByDate(room, date):
    local_timezone = tzlocal.get_localzone()
    datemsglist = []
    for message in room.messages:
        utcmsgdate = message[u'created']
        utcmsgdate = iso8601.parse_date(utcmsgdate)
        msgdate = utcmsgdate.replace(tzinfo=pytz.utc).astimezone(local_timezone)
        msgdate = msgdate.date()
        if date == msgdate:
            # print message[u'personEmail'], ": ", message[u'text']
            datemsglist.append(message)
    return datemsglist


def buildEmailBody(room, date):
    body = "Here is what you may have missed yesterday in %s, %s-%s-%s:\n" \
           % (room.title, date.month, date.day, date.year)
    local_timezone = tzlocal.get_localzone()
    messages = msgByDate(room, date)

    for message in reversed(messages):
        if 'text' in message.keys():
            utcmsgtime = message['created']
            utcmsgtime = iso8601.parse_date(utcmsgtime)
            localmsgtime = utcmsgtime.replace(tzinfo=pytz.utc).astimezone(local_timezone)
            timestamp = str(localmsgtime.hour) + ":" +str(localmsgtime.minute) + ":" + str(localmsgtime.second)
            displayname = getDisplayName(message['personId'], room.users)
            body = body + "%s - %s: %s \n" % (timestamp, displayname, message['text'])

    body = body.encode('utf-8')

    return body


def sendEmail(room, date):
    sender = os.environ['SENDER']
    #server = os.environ['SERVER']

    #server_port = os.environ['SERVER_PORT']

    ###Build list of user email addresses
    userarray = []
    for user in room.users:
        for email in user.emails:
            #if email not in config.ignorelist:
            userarray.append(email)

    msg = MIMEMultipart()
    body = MIMEText(str(buildEmailBody(room, date)).strip())

    msg['Subject'] = "Daily Spark Summary for %s" % room.title
    msg['From'] = sender
    msg['To'] = ", ".join(userarray)
    msg.attach(body)

    print msg

    #smtpObj = smtplib.SMTP(server, server_port)
    #smtpObj.sendmail(msg["From"], msg["To"].split(","), msg.as_string())

    #Gmail Settings
    server = smtplib.SMTP()
    server.connect('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    userid=os.environ['GMAIL_USERID']
    passwd=os.environ['GMAIL_PASSWORD']
    server.login(userid,passwd)
    server.sendmail(msg["From"], msg["To"].split(","), msg.as_string())

    print "email sent"

    return

if __name__ == "__main__":
    today = datetime.datetime.now().date()
    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).date()

    date = yesterday

    sendEmail(room, date)

