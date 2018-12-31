Twitter Webhook Examples
=============================

This example app shows how easy it is to implement the Twitter Webhooks API Adapter
to receive Twitter Webhook events

🤖  Setup and running the app
------------------------------

**Set up your Python environment:**

We're using virtualenv to keep the dependencies and environmental variables specific to this app. See `virtualenv`_ docs for more info.

.. _virtualenv: https://virtualenv.pypa.io

This example app works best in Python 2.7. If 2.7 is your default version, create a virtual environment by running:

.. code::

  virtualenv env

Otherwise, if Python 3+ is your default, specify the path to your 2.7 instance:

.. code::

  virtualenv -p /your/path/to/python2 env

Then initialize the virtualenv:

.. code::

  source env/bin/activate


**Install the app's dependencies:**

.. code::

  pip install -r requirements.txt


**🤖  Start ngrok**

In order for Twitter to contact your local server, you'll need to run a tunnel. We
recommend ngrok or localtunnel. We're going to use ngrok for this example.

If you don't have ngrok, `download it here`_.

.. _download it here: https://ngrok.com


Here's a rudimentary diagream of how ngrok allows Twitter to connect to your server

.. image:: https://cloud.githubusercontent.com/assets/32463/25376866/940435fa-299d-11e7-9ee3-08d9427417f6.png


💡  Twitter requires event requests be delivered over SSL, so you'll want to
    use the HTTPS URL provided by ngrok.

Run ngrok and copy the **HTTPS** URL

.. code::

  ngrok http 3000

.. code::

  ngrok by @inconshreveable (Ctrl+C to quit)

  Session status                      online
  Version                             2.1.18
  Region                  United States (us)
  Web Interface        http://127.0.0.1:4040

  Forwarding http://h7465j.ngrok.io -> localhost:9292
  Forwarding https://h7465j.ngrok.io -> localhost:9292

**🤖  Run the app:**

You'll need to have your server and ngrok running to complete your app's Event
Subscription setup

.. code::

  python example.py



🤔  Support
------------

Need help? Open an issue or bug @Roach on Twitter
