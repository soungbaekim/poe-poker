"""

Demo bot: catbot.

This bot uses all options provided by the Poe protocol. You can use it to get examples
of all the protocol has to offer.

"""

from __future__ import annotations

import asyncio
from typing import AsyncIterable

import fastapi_poe as fp
from modal import Image, Stub, Volume, asgi_app


import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Fetch the service account key JSON file contents
# cred = credentials.Certificate('path/to/serviceAccountKey.json')




class PokerBot(fp.PoeBot):
    async def get_response(
        self, request: fp.QueryRequest
    ) -> AsyncIterable[fp.PartialResponse]:
        """Return an async iterator of events to send to the user."""
        print(request)

        cred = credentials.Certificate('/firebase/key.json')

        # Initialize the app with a None auth variable, limiting the server's access
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://poe-poker-default-rtdb.firebaseio.com',
            'databaseAuthVariableOverride': None
        })

        # The app only has access to public data as defined in the Security Rules
        ref = db.reference('/hello')
        print(ref.get())

        last_message = request.query[-1].content.lower()
        response_content_type = (
            "text/plain" if "plain" in last_message else "text/markdown"
        )
        yield fp.MetaResponse(
            text="",
            content_type=response_content_type,
            linkify=True,
            refetch_settings=False,
            suggested_replies="dog" not in last_message,
        )

    async def on_feedback(self, feedback_request: fp.ReportFeedbackRequest) -> None:
        """Called when we receive user feedback such as likes."""
        print(
            f"User {feedback_request.user_id} gave feedback on {feedback_request.conversation_id}"
            f"message {feedback_request.message_id}: {feedback_request.feedback_type}"
        )

    async def get_settings(self, setting: fp.SettingsRequest) -> fp.SettingsResponse:
        """Return the settings for this bot."""
        return fp.SettingsResponse(
            allow_user_context_clear=True, allow_attachments=True
        )


REQUIREMENTS = ["fastapi-poe==0.0.36", "firebase-admin"]
image = Image.debian_slim().pip_install(*REQUIREMENTS)
stub = Stub("pokerbot-poe")

vol = Volume.from_name("firebase")

@stub.function(image=image, volumes={"/firebase": vol})
# @stub.function(volumes={"/firebase": vol})
@asgi_app()
def fastapi_app():
    bot = PokerBot()
    # Optionally, provide your Poe access key here:
    # 1. You can go to https://poe.com/create_bot?server=1 to generate an access key.
    # 2. We strongly recommend using a key for a production bot to prevent abuse,
    # but the starter examples disable the key check for convenience.
    # 3. You can also store your access key on modal.com and retrieve it in this function
    # by following the instructions at: https://modal.com/docs/guide/secrets
    # POE_ACCESS_KEY = ""
    # app = make_app(bot, access_key=POE_ACCESS_KEY)
    app = fp.make_app(bot, allow_without_key=True)
    return app
