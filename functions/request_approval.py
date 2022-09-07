import os
import logging

from datetime import datetime

from slack_sdk import WebClient
from slack_bolt import App, Complete, Ack

APPROVE_ID = "approve_action_id"
DENY_ID = "deny_action_id"

# Initialization
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
logging.basicConfig(level=logging.INFO)

# Register & define Listeners
@app.function("review_approval")
def request_approval(event, client: WebClient, complete: Complete, logger: logging.Logger):
    try:
        manager, employee, start_date, end_date = _parse_inputs(event["inputs"])
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


@request_approval.action(APPROVE_ID)
def approve_action(
    ack: Ack, client: WebClient, body: dict, complete: Complete, logger: logging.Logger
):
    try:
        ack()
        manager, employee, start_date, end_date = _parse_inputs(body["function_data"]["inputs"])
        markdown = (
            f":white_check_mark: Time-off request for _{start_date}_ :arrow_right: "
            f"_{end_date}_ approved by <@{manager}>"
        )
        context_block = _get_context_block(markdown)
        client.chat_postMessage(channel=employee, text=markdown, blocks=[context_block])

        _update_request_message(client, body, context_block, markdown)
        complete()
    except Exception as e:
        logger.error(e)
        complete(error="Cannot approve request")
        raise e


@request_approval.action(DENY_ID)
def deny_action(ack: Ack, client: WebClient, body, complete: Complete, logger: logging.Logger):
    try:
        ack()
        manager, employee, start_date, end_date = _parse_inputs(body["function_data"]["inputs"])
        markdown = (
            f":no_entry: Time-off request for _{start_date}_ :arrow_right: "
            f"_{end_date}_ denied by <@{manager}>"
        )
        context_block = _get_context_block(markdown)
        client.chat_postMessage(channel=employee, text=markdown, blocks=[context_block])

        _update_request_message(client, body, context_block, markdown)
        complete()
    except Exception as e:
        logger.error(e)
        complete(error="Cannot deny request")
        raise e


def _update_request_message(client: WebClient, body: dict, block: dict, text: str):
    updated_blocks = body["message"]["blocks"][:-1]
    updated_blocks.append(block)

    client.chat_update(
        channel=body["container"]["channel_id"],
        ts=body["container"]["message_ts"],
        text=text,
        blocks=updated_blocks,
    )


def _get_context_block(markdown: str) -> dict:
    return {
        "type": "context",
        "elements": [
            {
                "type": "mrkdwn",
                "text": markdown,
            },
        ],
    }


def _parse_inputs(inputs: dict):
    manager = inputs["manager"]
    employee = inputs["employee"]
    start_date = datetime.fromtimestamp(inputs["start_date"]).strftime("%m/%d/%Y %H:%M")
    end_date = datetime.fromtimestamp(inputs["end_date"]).strftime("%m/%d/%Y %H:%M")
    return manager, employee, start_date, end_date
