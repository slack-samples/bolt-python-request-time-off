from logging import Logger

from slack_sdk import WebClient
from slack_bolt import Complete

from .utils import APPROVE_ID, DENY_ID, parse_inputs


def request_approval(event, client: WebClient, complete: Complete, logger: Logger):
    try:
        manager, employee, start_date, end_date = parse_inputs(event["inputs"])
        client.chat_postMessage(
            channel=manager,
            text="A new time-off request has been submitted.",
            blocks=[
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "A new time-off request has been submitted",
                    },
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*From: * <@{employee}>",
                    },
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Dates: * _{start_date}_ :arrow_right: _{end_date}_",
                    },
                },
                {
                    "type": "actions",
                    "block_id": "approve-deny-buttons",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Approve",
                            },
                            "action_id": APPROVE_ID,
                            "style": "primary",
                        },
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Deny",
                            },
                            "action_id": DENY_ID,
                            "style": "danger",
                        },
                    ],
                },
            ],
        )
    except Exception as e:
        logger.error(e)
        complete(error="Cannot request approval")
        raise e
