import json
from flask import Flask
import pytest
from twitterwebhooks import TwitterWebhookAdapter
from twitterwebhooks.server import TwitterWebhookAdapterException


def test_existing_flask():
    valid_flask = Flask(__name__)
    valid_adapter = TwitterWebhookAdapter("CONSUMER_SECRET", "/webhooks/twitter", valid_flask)
    assert isinstance(valid_adapter, TwitterWebhookAdapter)


def test_server_not_flask():
    with pytest.raises(TypeError) as e:
        invalid_flask = "I am not a Flask"
        TwitterWebhookAdapter("CONSUMER_SECRET", "/webhooks/twitter", invalid_flask)
    assert e.value.args[0] == 'Server must be an instance of Flask'


def test_event_endpoint_get(client):
    # GET on '/webhooks/twitter' should 404
    res = client.get('/webhooks/twitter')
    assert res.status_code == 404

# TODO: Update this test for Twitter webhook registration handshake
# def test_url_challenge(client):
#     adapter = TwitterWebhookAdapter("CONSUMER_SECRET")
#     data = bytes(pytest.twitter_like_event_fixture, 'ascii')
#     signature = pytest.create_signature(adapter.consumer_secret, data)
#
#     res = client.post(
#         '/webhooks/twitter',
#         data=data,
#         content_type='application/json',
#         headers={
#             'X-Twitter-Webhooks-Signature': signature
#         }
#     )
#     assert res.status_code == 200
#     assert bytes.decode(res.data) == "valid_challenge_token"


def test_invalid_request_signature(client):
    # Verify [package metadata header is set
    adapter = TwitterWebhookAdapter("CONSUMER_SECRET")

    data = bytes(pytest.twitter_like_event_fixture, 'ascii')
    signature = "bad signature"

    with pytest.raises(TwitterWebhookAdapterException) as excinfo:
        res = client.post(
            '/webhooks/twitter',
            data=data,
            content_type='application/json',
            headers={
                'X-Twitter-Webhooks-Signature': signature
            }
        )

    assert str(excinfo.value) == 'Invalid request signature'


def test_server_start(mocker):
    # Verify server started with correct params
    adapter = TwitterWebhookAdapter("CONSUMER_SECRET")
    mocker.spy(adapter , 'server')
    adapter.start(port=3000)
    adapter.server.run.assert_called_once_with(debug=False, host='127.0.0.1', port=3000)


def test_default_exception_msg(mocker):
    with pytest.raises(TwitterWebhookAdapterException) as excinfo:
        raise TwitterWebhookAdapterException

    assert str(excinfo.value) == 'An error occurred in the TwitterWebhookAdapter library'
