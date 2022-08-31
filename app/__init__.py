
import os
import logging

from slack_bolt import App

# Initialization
# app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
app = App(token="xoxb-3655306058214-3951784469141-lcAIffuYwio2LutRS3jnx8Lh")
logging.basicConfig(level=logging.DEBUG)

# Register Listeners
from app.functions import app

__all__ = [
    "app",
]