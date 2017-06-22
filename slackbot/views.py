from django.shortcuts import render
import os
import requests
import json
from django.http import HttpResponse
from .models import Team
from .listen import Listener



# Create your views here.
def index(request):
    client_id = os.environ.get('SLACK_CLIENT_ID')
    return render(request, 'landing.html', {'client_id': client_id})


def slack_oauth(request):
    code = request.GET['code']

    params = {
        'code': code,
        'client_id': os.environ.get('SLACK_CLIENT_ID'),
        "client_secret": os.environ.get('SLACK_CLIENT_SECRET')
    }
    url = 'https://slack.com/api/oauth.access'
    json_response = requests.get(url, params)
    data = json.loads(json_response.text)
    Team.objects.get_or_create(
        name=data['team_name'],
        team_id=data['team_id'],
        bot_user_id=data['bot']['bot_user_id'],
        bot_access_token=data['bot']['bot_access_token'],
    )
    return HttpResponse('Bot added to your Slack team!')

#send messages to slack and listen to events in real time.
Listener.handle()
channel_name=Listener.Listen_to_channel()
print(channel_name)
