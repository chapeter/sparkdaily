from spark import ROOM
import boto3
import sparkdaily
import os



token = os.environ['SPARK_TOKEN']
#room = os.environ['SPARK_ROOM']
auth = "Bearer %s" % token

db = boto3.resource('dynamodb', region_name='us-east-1')
table = db.Table('sparkrooms')

rooms = table.scan()[u'Items']

for room in rooms:
    roomid = room[u'roomid']
    sparkroom = ROOM(auth, roomid)
    print "Working on %s" % sparkroom.getRoomTitle
    sparkdaily.run(sparkroom)
