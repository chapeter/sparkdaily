import config
import datetime
import requests
import json
import iso8601
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

token = config.token
auth = "Bearer %s" % token
room = config.roomid
ignorelist = config.ignorelist
date = datetime.datetime.now().date()


def getMessages():
    url = "https://api.ciscospark.com/v1/messages"
    querystring = {"roomId": room}

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
    messages = getMessages()
    todaymsg_list = []
    for message in messages:
        msgdate = message[u'created']
        msgdate = iso8601.parse_date(msgdate).date()
        if date == msgdate:
            #print message[u'personEmail'], ": ", message[u'text']
            todaymsg_list.append(message)
    return todaymsg_list

def createEmailBody(msg_list):
    body = ""
    for message in msg_list:
        #body = body , str(message[u'personEmail']), ": ", str(message[u'text']), "\n"
        body = body + "%s : %s \n" % (str(message[u'personEmail']), str(message[u'text']))
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
        user_list.append(str(user['personEmail']))
    return user_list


sender = config.sender
server = config.server
server_port = config.server_port

msg = MIMEMultipart()
body = MIMEText(str(createEmailBody(todayMessage())).strip())

msg['Subject'] = "Daily Summary"
msg['From'] = sender
msg['To'] = ", ".join(getUsers())
msg.attach(body)


smtpObj = smtplib.SMTP(server, server_port)
smtpObj.sendmail(msg["From"], msg["To"].split(","), msg.as_string())




