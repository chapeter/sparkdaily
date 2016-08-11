__author__ = 'Chad Peterson'
__email__ = 'chapeter@cisco.com'

import config
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
<<<<<<< HEAD
from spark import ROOM
import iso8601
import tzlocal
import pytz
import datetime
=======
import pytz
import tzlocal
import sys
>>>>>>> master

token = config.token
auth = "Bearer %s" % token
room = config.roomid
ignorelist = config.ignorelist
<<<<<<< HEAD
yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).date()
today = datetime.datetime.now()
date = today
sender = config.sender
server = config.server
server_port = config.server_port
room = ROOM(auth, room)
=======
date = (datetime.datetime.now() - datetime.timedelta(days=1)).date()
local = pytz.timezone("America/Chicago")


def getMessages():
    url = "https://api.ciscospark.com/v1/messages"
    querystring = {"roomId": room,
                   "max" : 50}

    headers = {
        'authorization': auth,
        'cache-control': "no-cache",
        'content-type': 'application/json'
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    messages = json.loads(response.content)
    messages = messages[u'items']

    return messages

def todayMessage():
    date = (datetime.datetime.now() - datetime.timedelta(days=1)).date()
    local_timezone = tzlocal.get_localzone()
    messages = getMessages()
    todaymsg_list = []
    for message in messages:
        utcmsgdate = message[u'created']
        utcmsgdate = iso8601.parse_date(utcmsgdate)
        msgdate = utcmsgdate.replace(tzinfo=pytz.utc).astimezone(local_timezone)
        msgdate = msgdate.date()
        if date == msgdate:
            #print message[u'personEmail'], ": ", message[u'text']
            todaymsg_list.append(message)
    if len(todaymsg_list) == 0:
        sys.exit("No Messages to send")
    return todaymsg_list

def createEmailBody(msg_list, roomId):
    body = "Here is what you may have missed yesterday in %s, %s-%s-%s:\n" \
           % (roomtitle, date.month, date.day, date.year)
    for message in reversed(msg_list):
        #body = body , str(message[u'personEmail']), ": ", str(message[u'text']), "\n"
        msgtime = str(iso8601.parse_date(message[u'created']).time().hour) + ":" +\
                  str(iso8601.parse_date(message[u'created']).time().minute) + ":" + \
                  str(iso8601.parse_date(message[u'created']).time().second)
        #body = body + "%s - %s:  \n" % (str(msgtime), str(message[u'personEmail']))
        body = body + "%s - %s: %s \n" % (str(msgtime), getDisplayName(message[u'personId']),
                                          message[u'text'])
    body = body + "\n\nJoin the chat - https://web.ciscospark.com/#rooms/%s" % getRoomURL(roomId)
    body = body.encode('utf-8').strip()
    return body

def getUsers():
    url = "https://api.ciscospark.com/v1/memberships"
    querystring = {"roomId": room}

    headers = {
        'authorization': auth,
        'cache-control': "no-cache",
        'content-type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    users = json.loads(response.content)
    users = users[u'items']
    user_list = []
    for user in users:
        ##Ignore monitor bots
        if user[u'isMonitor'] == False:
            user_list.append(str(user['personEmail']))
    return user_list

def getDisplayName(personId):
    url = "https://api.ciscospark.com/v1/people/" + personId
>>>>>>> master


def getDisplayName(personId, users):
    for user in users:
        if user.personId == personId:
            return user.displayname
    return "userID not found"


<<<<<<< HEAD
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
        print body
=======
    headers = {
        'authorization': auth,
        'cache-control': "no-cache",
        'content-type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers)
    roominfo = json.loads(response.content)
    title = str(roominfo[u'title'])
>>>>>>> master

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


<<<<<<< HEAD
if __name__ == "__main__":
    sendEmail(room)
=======
smtpObj = smtplib.SMTP(server, server_port)
smtpObj.sendmail(msg["From"], msg["To"].split(","), msg.as_string())
>>>>>>> master
