from slack_bolt import App
from slack_bolt.slack_function import SlackFunction

from functions.utils import APPROVE_ID, DENY_ID
from functions.request_approval import request_approval
from functions.actions import approve_action, deny_action


def register_functions(app: App):
    """Takes Bolt App and registers a slack function to it,
    once the function is registered is uses the returned
    SlackFunction object to attach interactivity actions to it

    Args:
        app (App): Bolt application instance
    """
    sample_view_func: SlackFunction = app.function("review_approval")(request_approval)
    sample_view_func.action(APPROVE_ID)(approve_action)
    sample_view_func.action(DENY_ID)(deny_action)
