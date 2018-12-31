import json
from base64 import b64encode, b64decode
from hashlib import sha256
import hmac
import pytest
from twitterwebhooks import TwitterWebhookAdapter


def create_signature(consumer_secret, request_data):
    h = hmac.new(
        bytes(consumer_secret, 'utf-8'),
        request_data,
        digestmod=sha256
    )
    return "sha256={}".format(b64encode(h.digest()).decode("utf-8"))


def load_event_fixture(event, as_string=True):
    filename = "tests/data/{}.json".format(event)
    with open(filename) as json_data:
        event_data = json.load(json_data)
        if not as_string:
            return event_data
        else:
            return json.dumps(event_data)


def event_with_bad_token():
    event_data = load_event_fixture('twitter_like_event', as_string=False)
    event_data['token'] = "bad_token"
    return json.dumps(event_data)


def pytest_namespace():
    return {
        'twitter_like_event_fixture': load_event_fixture('twitter_like_event'),
        'url_challenge_fixture': load_event_fixture('url_challenge'),
        'bad_token_fixture': event_with_bad_token(),
        'create_signature': create_signature
    }


@pytest.fixture
def app():
    adapter = TwitterWebhookAdapter("CONSUMER_SECRET")
    app = adapter.server
    app.testing = True
    return app
