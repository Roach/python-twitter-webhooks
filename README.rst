Twitter Webhook adapter for Python
===================================

.. image:: https://travis-ci.org/slackapi/python-slack-events-api.svg?branch=master
    :target: https://travis-ci.org/slackapi/python-slack-events-api
.. image:: https://codecov.io/gh/slackapi/python-slack-events-api/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/slackapi/python-slack-events-api


The Twitter Webhook Adapter is a Python-based solution to receive and parse events
from Twitter's Webhook API. This library uses an event emitter framework to allow
you to easily process Twitter events by simply attaching functions
to event listeners.

This adapter enhances and simplifies Twitter's Webhook API by incorporating useful best practices, patterns, and opportunities to abstract out common tasks.

💡  This project is based on  `Slack's Events API Adapter for Python`_ .

.. _Slack's Events API Adapter for Python: https://github.com/slackapi/python-slack-events-api

⚠️ This project hasn't been tested in Python 2.


🤖  Installation
----------------

.. code:: shell

  pip install twitterwebhooks


**🎉 Once your webhook has been registered and user subscriptions are set up, you will begin receiving Twitter Events**

    ⚠️  Ngrok is a great tool for developing Webhook style apps, but it's not recommended to use ngrok
    for production apps.

🤖  Usage
----------
  **⚠️  Keep your app's credentials safe!**

  - For development, keep them in virtualenv variables.

  - For production, use a secure data store.

  - Never post your app's credentials to github.

.. code:: python

  TWITTER_CONSUMER_SECRET = os.environ["TWITTER_CONSUMER_SECRET"]

Create a Webhook server for receiving actions via the Events API
-----------------------------------------------------------------------
**Using the built-in Flask server:**

.. code:: python

  from twitterwebhoooks import TwitterWebhookAdapter

  events_adapter = TwitterWebhookAdapter(CONSUMER_SECRET, "/webhooks/twitter")


  @events_adapter.on("favorite_events")
  def handle_message(event_data):
      event = event_data['event']
      faved_status = event['favorited_status']
      faved_status_id = faved_status['id']
      faved_status_screen_name = faved_status['user']['screen_name']
      faved_by_screen_name = event['user']['screen_name']
      print("@{} faved @{}'s tweet: {}".format(faved_by_screen_name, faved_status_screen_name, faved_status_id))
      print(json.dumps(event_data, indent=4, sort_keys=True))


   # Start the server on port 3000
   events_adapter.start(port=3000)


**Using your existing Flask instance:**


.. code:: python

  from flask import Flask
  from twitterwebhoooks import TwitterWebhookAdapter


  # This `app` represents your existing Flask app
  app = Flask(__name__)


  # An example of one of your Flask app's routes
  @app.route("/")
  def hello():
    return "Hello there!"


  # Bind the Events API route to your existing Flask app by passing the server
  # instance as the last param, or with `server=app`.
  events_adapter = TwitterWebhookAdapter(CONSUMER_SECRET, "/webhooks/twitter", app)


  @events_adapter.on("favorite_events")
  def handle_message(event_data):
      event = event_data['event']
      faved_status = event['favorited_status']
      faved_status_id = faved_status['id']
      faved_status_screen_name = faved_status['user']['screen_name']
      faved_by_screen_name = event['user']['screen_name']
      print("@{} faved @{}'s tweet: {}".format(faved_by_screen_name, faved_status_screen_name, faved_status_id))
      print(json.dumps(event_data, indent=4, sort_keys=True))


  # Start the server on port 3000
  if __name__ == "__main__":
    app.run(port=3000)


🤖  Example event listeners
-----------------------------

See `example.py`_ for usage examples.

.. _example.py: /example/

🤔  Support
-----------

Need help? Open an issue or bug @Roach on Twitter
