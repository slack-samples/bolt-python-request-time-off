import os

from slack_bolt.adapter.socket_mode import SocketModeHandler

from app import app

from app.listeners.functions import request_approval

# Start Bolt app
if __name__ == "__main__":
    print(app._listeners)
    # SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()
