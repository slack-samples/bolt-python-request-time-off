import os
from slack_bolt.adapter.socket_mode import SocketModeHandler

from functions import app

# Start Bolt app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()
