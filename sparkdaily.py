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
from dateutil import tz




token = os.environ['SPARK_TOKEN']
room = os.environ['SPARK_ROOM']
auth = "Bearer %s" % token
room = ROOM(auth, room)





def getDisplayName(personId, users):
    for user in users:
        if user.personId == personId:
            return user.displayname
    return "userID not found"

def shiftToLocal(date, timezone):
    from_zone = tz.gettz('UTC')
    to_zone = timezone

    utc = iso8601.parse_date(date)
    utc = utc.replace(tzinfo=from_zone)
    local = utc.astimezone(to_zone)

    return local

def msgByDate(room, date, timezone):
    datemsglist = []

    from_zone = tz.gettz('UTC')
    to_zone = timezone

    count = 1
    for message in room.getMsgBeforeDate(date):
        utc = iso8601.parse_date(message[u'created'])
        utc = utc.replace(tzinfo=from_zone)
        local = utc.astimezone(to_zone)

        print str(count), date, local.date(), message
        count = count+1
        if date == local.date():
            #print message[u'personEmail'], ": ", message[u'text']
            datemsglist.append(message)
    return datemsglist


def buildEmailBody(room, date, timezone):
    body = "Here is what you may have missed yesterday in %s, %s-%s-%s:\n" \
           % (room.title, date.month, date.day, date.year)
    messages = msgByDate(room, date, timezone)

    for message in reversed(messages):
        if u'text' in message.keys():
            localmsgtime = shiftToLocal(message[u'created'], timezone)
            timestamp = str(localmsgtime.hour) + ":" +str(localmsgtime.minute) + ":" + str(localmsgtime.second)
            displayname = getDisplayName(message['personId'], room.users)
            body = body + "%s - %s: %s \n" % (timestamp, displayname, message['text'])

    body = body.encode('utf-8')

    return body


def sendEmail(room, date, timezone):
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
    body = MIMEText(str(buildEmailBody(room, date, timezone)).strip())

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

    #today = datetime.datetime.now().date()
    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).date()
    #yesterdayiso = (datetime.datetime.now() - datetime.timedelta(days=1))
    timezone = tz.gettz("America/Chicago")

    date = yesterday


    sendEmail(room, date, timezone)

