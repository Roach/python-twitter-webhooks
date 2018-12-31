from flask import Flask, request, make_response
import base64
from hashlib import sha256
import hmac
import json


class WebhookServer(Flask):

    def __init__(self, consumer_secret, endpoint, emitter, server):
        self.consumer_secret = consumer_secret
        self.emitter = emitter
        self.endpoint = endpoint

        # If a server is passed in, bind the event handler routes to it,
        # otherwise create a new Flask instance.
        if server:
            if isinstance(server, Flask):
                self.bind_route(server)
            else:
                raise TypeError("Server must be an instance of Flask")
        else:
            Flask.__init__(self, __name__)
            self.bind_route(self)

    def create_signature(self, crc):
        # Generate CRC signature to confirm webhook URL
        validation = hmac.new(
            key=bytes(self.consumer_secret, 'utf-8'),
            msg=bytes(crc, 'utf-8'),
            digestmod=sha256
        )
        digested = base64.b64encode(validation.digest())
        response = {
            'response_token': 'sha256=' + format(str(digested)[2:-1])
        }

        return json.dumps(response)

    def verify_request(self, request_data):
        signature = request.headers["X-Twitter-Webhooks-Signature"]
        try:
            crc = base64.b64decode(signature[7:])  # strip out the first 7 characters
            h = hmac.new(
                bytes(self.consumer_secret, 'ascii'),
                request_data,
                digestmod=sha256
            )
            return hmac.compare_digest(h.digest(), crc)
        except base64.binascii.Error as err:
            return False

    def bind_route(self, server):
        @server.route(self.endpoint, methods=['GET'])
        def crc_handshake():
            if "crc_token" in request.args:
                crc = request.args['crc_token']
                self.emitter.emit("crc", crc)
                return make_response(self.create_signature(crc), 200)
            else:
                return make_response("These are not the twitter bots you're looking for.", 404)

        @server.route(self.endpoint, methods=['POST'])
        def event():
            # Verify the request signature using the app's signing secret
            # emit an error if the signature can't be verified
            if not self.verify_request(request.get_data()):
                twtr_exception = TwitterWebhookAdapterException('Invalid request signature')
                self.emitter.emit('error', twtr_exception)
                return make_response("", 403)

            # Parse the Event payload and emit the event to the event listener
            request_json = request.get_json()
            for event_type in filter(lambda events: '_event' in events, list(request_json)):
                for specific_event in request_json[event_type]:
                    event_data = {
                        'for_user_id': int(request_json['for_user_id']),
                        'event': specific_event,
                    }
                    if 'users' in request_json:
                        event_data['users'] = request_json['users']

                    self.emitter.emit(event_type, event_data)
                    self.emitter.emit('any', request_json)
            response = make_response("", 200)
            return response


class TwitterWebhookAdapterException(Exception):
    """
    Base exception for all errors raised by the TwitterWebhookAdapter library
    """
    def __init__(self, msg=None):
        if msg is None:
            # default error message
            msg = "An error occurred in the TwitterWebhookAdapter library"
        super(TwitterWebhookAdapterException, self).__init__(msg)
