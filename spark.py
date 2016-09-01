__author__ = 'Chad Peterson'
__email__ = 'chapeter@cisco.com'
import base64
import requests
import json
import iso8601
import datetime
import pytz
import tzlocal
import sys



class ROOM(object):
    """
    Class used for creating rooms
    """

    def __init__(self, auth, roomId):
        self.auth = auth
        self.roomId = roomId
        self.title = self.getRoomTitle
        self.urlid = self.getRoomURL
        self.users = self.getUsers
        self.messages = self.getMessages



    @property
    def getRoomTitle(self):
        url = "https://api.ciscospark.com/v1/rooms/" + self.roomId

        headers = {
            'authorization': self.auth,
            'cache-control': "no-cache",
            'content-type': 'application/json'
        }
        response = requests.request("GET", url, headers=headers)
        roominfo = json.loads(response.content)
        title = str(roominfo[u'title'])
        return title

    @property
    def getRoomURL(self):
        basedecode = base64.b64decode(self.roomId)
        roomurl = basedecode.split('/')[-1]
        return roomurl

    @property
    def getUsers(self):
        url = "https://api.ciscospark.com/v1/memberships"
        querystring = {"roomId": self.roomId}

        headers = {
            'authorization': self.auth,
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
                #user_list.append(str(user['personId']))
                user_list.append(USER(self.auth, user['personId']))

        return user_list

    @property
    def getMessages(self):
        #date = datetime.datetime.now().date()
        #date = (datetime.datetime.now() - datetime.timedelta(days=1)).date()
        local_timezone = tzlocal.get_localzone()

        url = "https://api.ciscospark.com/v1/messages"
        querystring = {"roomId": self.roomId,
                       "max": 50}

        headers = {
            'authorization': self.auth,
            'cache-control': "no-cache",
            'content-type': 'application/json'
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        messages = json.loads(response.content)
        messages = messages[u'items']
        #todaymsg_list = []
        todaymsg_list = messages
        #for message in messages:
        #    utcmsgdate = message[u'created']
        #    utcmsgdate = iso8601.parse_date(utcmsgdate)
        #    msgdate = utcmsgdate.replace(tzinfo=pytz.utc).astimezone(local_timezone)
        #    msgdate = msgdate.date()
        #    if date == msgdate:
        #        # print message[u'personEmail'], ": ", message[u'text']
        #        todaymsg_list.append(message)
        if len(todaymsg_list) == 0:
            sys.exit("No Messages to send")
        return todaymsg_list



class USER(object):
    def __init__(self, auth, personId):
        self.auth = auth
        self.personId = personId
        self.emails = []
        self.emails = self.getEmails()
        self.displayname = self.getDisplayName()


    def getEmails(self):
        emails = self.getUserInfo()[u'emails']
        return emails

    def getDisplayName(self):
        displayname = str(self.getUserInfo()['displayName'])
        return displayname

    def getUserInfo(self):
        url = "https://api.ciscospark.com/v1/people/" + self.personId

        headers = {
            'authorization': self.auth,
            'cache-control': "no-cache",
            'content-type': 'application/json'
        }
        response = requests.request("GET", url, headers=headers)
        userinfo = json.loads(response.content)

        return userinfo



class MESSAGE(object):
    def __init__(self, message):
        for key in message:
            setattr(self, key, message[key])


