import pytest
from twitterwebhooks import TwitterWebhookAdapter

ADAPTER = TwitterWebhookAdapter('CONSUMER_SECRET', '/webhooks/twitter')


def test_event_emission(client):
    # Events should trigger an event
    @ADAPTER.on('reaction_added')
    def event_handler(event):
        assert event["reaction"] == 'grinning'

    data = bytes(pytest.twitter_like_event_fixture, 'ascii')
    signature = pytest.create_signature(ADAPTER.consumer_secret, data)
    res = client.post(
        '/webhooks/twitter',
        data=data,
        content_type='application/json',
        headers={
            'X-Twitter-Webhooks-Signature': signature
        }
    )

    assert res.status_code == 200
