__author__ = 'Chad Peterson'
__email__ = 'chapeter@cisco.com'
import base64
import requests


class ROOM(object):
    """
    Class used for creating rooms
    """

    def __init__(self, auth, roomId):
        self.auth = auth
        self.roomId = roomId
        self.title = getRoomTitle()
        self.urlid = getRoomURL()
        self.users = getUsers()




    def getRoomTitle(self, roomId):
        url = "https://api.ciscospark.com/v1/rooms/" + roomId

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
        basedecode = base64.b64decode(roomId)
        roomurl = basedecode.split('/')[-1]
        return roomurl

    @property
    def getUsers(self):
        url = "https://api.ciscospark.com/v1/memberships"
        querystring = {"roomId": roomId}

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
        return users