import slack
import os
import time
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, Response, make_response
from slackeventsapi import SlackEventAdapter

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)

slack_event_adapter = SlackEventAdapter(
    os.environ['SIGNING_SECRET_'], "/slack/events/", app)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

BOT_ID = client.api_call('auth.test')['user_id']



@ slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event',{})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    print("--->  ",channel_id,text)
    # if BOT_ID != user_id:
    client.chat_postMessage(channel=channel_id,text=text)


# client.chat_postMessage(channel="#bug",text="great")


if __name__ == '__main__':
    app.run(debug=True)

