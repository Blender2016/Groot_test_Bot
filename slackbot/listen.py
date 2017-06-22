from django.conf import settings
from slackclient import SlackClient
from slackbot.models import Team
import json
import os
import requests
import time




class Listener():

    def handle():
        team = Team.objects.first()
        client = SlackClient(team.bot_access_token)
        webhook_url=os.environ.get('SLACK_WEBHOOK_SECRET')
# -------------------------------------------------------------------------
        slack_data ={
                       "text": "new image",
                       "attachments": [
                                            {
                                                "text": "Optional text that appears within the attachment",
                                                "image_url": "https://www.cleverfiles.com/howto/wp-content/uploads/2016/08/mini.jpg",
                                                # "thumb_url": "https://en.wikipedia.org/wiki/Linux#/media/File:Tux.svg"
                                            }
                                        ]
                    }
        mesg_one={
                        "text": "Would you like to play a game?",
                        "attachments": [
                                    {
                                        "text": "Choose a game to play",
                                        "fallback": "You are unable to choose a game",
                                        "callback_id": "wopr_game",
                                        "color": "#3AA3E3",
                                        "attachment_type": "default",
                                        "actions": [
                                            {
                                                "name": "game",
                                                "text": "Chess",
                                                "type": "button",
                                                "value": "chess"
                                            },
                                            {
                                                "name": "game",
                                                "text": "Falken's Maze",
                                                "type": "button",
                                                "value": "maze"
                                            },
                                            {
                                                "name": "game",
                                                "text": "Thermonuclear War",
                                                "style": "danger",
                                                "type": "button",
                                                "value": "war",
                                                "confirm": {
                                                    "title": "Are you sure?",
                                                    "text": "Wouldn't you prefer a good game of chess?",
                                                    "ok_text": "Yes",
                                                    "dismiss_text": "No"
                                                }
                                            }
                                        ]
                                    }
                                ]
                    }
        mesg_two= {
    "text": "New comic book alert!",
    "attachments": [
        {
            "title": "The Further Adventures of Slackbot",
            "fields": [
                {
                    "title": "Volume",
                    "value": "1",
                    "short": True
                },
                {
                    "title": "Issue",
                    "value": "3",
                     "short": True
                }
            ],
            "author_name": "Stanford S. Strickland",
            "author_icon": "http://a.slack-edge.com/7f18https://a.slack-edge.com/bfaba/img/api/homepage_custom_integrations-2x.png",
            "image_url": "http://i.imgur.com/OJkaVOI.jpg?1"
        },
        {
            "title": "Synopsis",
            "text": "After @episod pushed exciting changes to a devious new branch back in Issue 1, Slackbot notifies @don about an unexpected deploy..."
        },
        {
            "fallback": "Would you recommend it to customers?",
            "title": "Would you recommend it to customers?",
            "callback_id": "comic_1234_xyz",
            "color": "#3AA3E3",
            "attachment_type": "default",
            "actions": [
                {
                    "name": "recommend",
                    "text": "Recommend",
                    "type": "button",
                    "value": "recommend"
                },
                {
                    "name": "no",
                    "text": "No",
                    "type": "button",
                    "value": "bad"
                }
            ]
        }
    ]
}
# ----------------------------------------------------------------------------
        if client.rtm_connect():
            while True:
                events = client.rtm_read()
                print("%s----%s" % (team, events))
                for event in events:
                    print (event)
                    if 'type' in event and event['type'] == 'message' and event['text'] == 'hi':
                        # client.rtm_send_message(event['channel'],"hello world")
                        client.api_call(
                                      "chat.postMessage",
                                      channel=event['channel'],
                                      text="Hello from Python! :tada:",
                                    )
                    elif 'type' in event and event['type'] == 'message' and event['text'] == 'image':
                          requests.post(
                                                   webhook_url, data=json.dumps(slack_data),
                                                   headers={'Content-Type': 'application/json'}
                                        )
                    elif 'type' in event and event['type'] == 'message' and event['text'] == 'button1':
                          requests.post(
                                                   webhook_url, data=json.dumps(mesg_one),
                                                   headers={'Content-Type': 'application/json'}
                                        )
                    elif 'type' in event and event['type'] == 'message' and event['text'] == 'button2':
                          requests.post(
                                                   webhook_url, data=json.dumps(mesg_two),
                                                   headers={'Content-Type': 'application/json'}
                                        )
                time.sleep(1)
