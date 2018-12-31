from TwitterAPI import TwitterAPI
from twitterwebhooks import TwitterWebhookAdapter
import os
import json

CONSUMER_KEY = os.environ.get('CONSUMER_KEY', None)
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET', None)
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN', None)
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET', None)

events_adapter = TwitterWebhookAdapter(CONSUMER_SECRET, "/webhooks/twitter")
twtr = TwitterAPI(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

logger = events_adapter.server.logger


def get_account_id():
    # Helper for fetching the bot's ID
    credentials = twtr.request('account/verify_credentials').json()
    return credentials['id']


def send_dm(recipient_id, message_text):
    # Helper for sending DMs
    event = {
            "event": {
                "type": "message_create",
                "message_create": {
                    "target": {
                        "recipient_id": recipient_id
                    },
                    "message_data": {
                        "text": message_text
                    }
                }
            }
    }

    r = twtr.request('direct_messages/events/new', json.dumps(event))
    response_json = r.json()
    return response_json


# Fetch the account's ID so we can optionally ignore
# messages sent from the bot
BOT_ID = get_account_id()


@events_adapter.on("direct_message_events")
def handle_message(event_data):
    event = event_data['event']
    if event['type'] == 'message_create':
        recipient_id = event['message_create']['target']['recipient_id']
        sender_id = event['message_create']['sender_id']
        sender_screen_name = event_data['users'][sender_id]['screen_name']
        recipient_screen_name = event_data['users'][recipient_id]['screen_name']
        message_text = event['message_create']['message_data']['text']

        # Filter out bot messages
        if str(sender_id) == str(BOT_ID):
            print("IGNORING [Event {}] Incoming DM: To {} from {} \"{}\"".format(
                event['id'],
                recipient_screen_name,
                sender_screen_name,
                message_text
            ))
        else:
            print("[Event {}] Incoming DM: To {} from {} \"{}\"".format(
                event['id'],
                recipient_screen_name,
                sender_screen_name,
                message_text
            ))
            try:
                dm_id = send_dm(sender_id, "ACK! {}".format(event['id']))['event']['id']
                print("Send DM: {}".format(dm_id))
            except Exception as e:
                print("An error occurred sending DM: {}".format(e))


@events_adapter.on("favorite_events")
def handle_message(event_data):
    event = event_data['event']
    faved_status = event['favorited_status']
    faved_status_id = faved_status['id']
    faved_status_screen_name = faved_status['user']['screen_name']
    faved_by_screen_name = event['user']['screen_name']
    print("@{} faved @{}'s tweet: {}".format(faved_by_screen_name, faved_status_screen_name, faved_status_id))
    print(json.dumps(event_data, indent=4, sort_keys=True))

@events_adapter.on("any")
def handle_message(event_data):
    # Loop through events array and log received events
    for s in filter(lambda x: '_event' in x, list(event_data)):
        print("[any] Received event: {}".format(s))


# Handler for error events
@events_adapter.on("error")
def error_handler(err):
    print("ERROR: " + str(err))


# Once we have our event listeners configured, we can start the
# Flask server with the default `/events` endpoint on port 3000
events_adapter.start(port=3000)
