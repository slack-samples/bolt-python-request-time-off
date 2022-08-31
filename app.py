from slack_bolt.adapter.socket_mode import SocketModeHandler

from app import app

# Start Bolt app
if __name__ == "__main__":
    print(app._listeners)
    # SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()
