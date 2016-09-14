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
import sys
from jinja2 import Environment, PackageLoader
#from premailer import transform



token = os.environ['SPARK_TOKEN']
room = os.environ['SPARK_ROOM']
auth = "Bearer %s" % token
room = ROOM(auth, room)



def timeFixUp(time):
    if time < 10:
        newtime = "0" + str(time)
    else:
        newtime = str(time)
    return newtime

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

        #print str(count), date, local.date(), message
        count = count+1
        if date == local.date():
            #print message[u'personEmail'], ": ", message[u'text']
            datemsglist.append(message)
    return datemsglist


def buildEmailBody(room, date, timezone):
    body = "Here is what you may have missed yesterday in %s, %s-%s-%s:\n" \
           % (room.title, date.month, date.day, date.year)
    messages = msgByDate(room, date, timezone)

    if len(messages) == 0:
        print "No messages to send"
        sys.exit(0)
    else:
        for message in reversed(messages):
            if u'text' in message.keys():
                localmsgtime = shiftToLocal(message[u'created'], timezone)
                timestamp = timeFixUp(localmsgtime.hour) + ":" + timeFixUp(localmsgtime.minute) + ":" + timeFixUp(localmsgtime.second)
                displayname = getDisplayName(message['personId'], room.users)
                body = body + "%s - %s: %s \n" % (timestamp, displayname, message['text'])

    body = body.encode('utf-8')

    return body

def buildHTML(room, date, timezone):
    datestring = str(date.month) +"/" + str(date.day) + "/" + str(date.year)
    messages = msgByDate(room, date,timezone)
    roomtitle = room.title
    if len(messages) == 0:
        print "no messages to send, exiting"
        sys.exit(0)
    else:
        for message in reversed(messages):
            if u'text' in message.keys():
                message['localmsgtime'] = shiftToLocal(message[u'created'], timezone)
                message['timestamp'] = timeFixUp(message['localmsgtime'].hour) + ":" + timeFixUp(message['localmsgtime'].minute) + ":" + timeFixUp(message['localmsgtime'].second)
                message['displayname'] = getDisplayName(message['personId'], room.users)

    env = Environment(loader=PackageLoader('sparkdaily', 'templates'))
    template = env.get_template('newsletter.html')
    html = template.render(roomtitle=roomtitle, messages=reversed(messages), datestring=datestring)
    #emailhtml = transform(html)
    emailhtml = (html)

    #print emailhtml

    return emailhtml


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

    msg = MIMEMultipart('alternitive')
    #textbody = MIMEText(str(buildEmailBody(room, date, timezone)).strip())
    htmlbody = MIMEText(buildHTML(room, date, timezone), 'html')

    #print htmlbody

    msg['Subject'] = "Daily Spark Summary for %s" % room.title
    msg['From'] = sender
    msg['To'] = ", ".join(userarray)
    #msg.attach(textbody)
    msg.attach(htmlbody)


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

