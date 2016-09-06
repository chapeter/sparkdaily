Sparkdaily is a Python application which will send an email of all the conversations that happened yesterday for a given room to all memebers.

Sparkdaily is curretly setup to use GMAIL as the outgoing SMTP server, but can easily be changed to any SMTP server.


#Getting Started

1. Get your spark API token here: https://developer.ciscospark.com/
2. Find your roomId here: https://developer.ciscospark.com/endpoint-rooms-get.html
3. Install requirements
```
pip install -r requirements.txt
```
4. Set environment variables
```
export SPARK_TOKEN=<YOUR SPARK TOKEN FROM STEP 1>
export SPARK_ROOM=<YOUR SPARK ROOM ID FROM STEP 2>
export SENDER=<YOUR EMAIL ADDRESS>
export GMAIL_USER=<YOUR GMAIL USER ACCOUNT>
export GMAIL_PASSWORD=<YOUR EMAIL PASSWORD>
```
5. Run the app
```python sparkdaily.py```
