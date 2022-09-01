from typing import Tuple
from datetime import datetime
from logging import Logger

from slack_sdk import WebClient
from slack_bolt import Complete, Ack

from app.setup import app


@app.function("review_approval")
def request_approval(event, client: WebClient, complete: Complete, logger: Logger):
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
                            "action_id": "approve_action_id",
                            "style": "primary",
                        },
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Deny",
                            },
                            "action_id": "deny_action_id",
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


@request_approval.action("approve_action_id")
def approve_action(ack: Ack, client: WebClient, body, complete: Complete, logger: Logger):
    try:
        ack()
        manager, employee, start_date, end_date = _parse_inputs(body["function_data"]["inputs"])
        mrkdwn = (
            f":white_check_mark: Time-off request for _{start_date}_ :arrow_right: "
            f"_{end_date}_ approved by <@{manager}>"
        )

        _notify_response(client, employee, body, mrkdwn)

        complete()
    except Exception as e:
        logger.error(e)
        complete("Cannot request approval")
        raise e


@request_approval.action("deny_action_id")
def deny_action(ack: Ack, client: WebClient, body, complete: Complete, logger: Logger):
    try:
        ack()
        manager, employee, start_date, end_date = _parse_inputs(body["function_data"]["inputs"])
        mrkdwn = (
            f":no_entry: Time-off request for _{start_date}_ :arrow_right: "
            f"_{end_date}_ denied by <@{manager}>"
        )

        _notify_response(client, employee, body, mrkdwn)

        complete()
    except Exception as e:
        logger.error(e)
        complete(error="Cannot request approval")
        raise e


def _notify_response(client: WebClient, employee: str, body: dict, mrkdwn: str):
    context_block = _get_context_block(mrkdwn)

    updated_blocks = body["message"]["blocks"][:-1]
    updated_blocks.append(context_block)

    client.chat_postMessage(channel=employee, text=mrkdwn, blocks=[context_block])

    client.chat_update(
        channel=body["container"]["channel_id"],
        ts=body["container"]["message_ts"],
        text=mrkdwn,
        blocks=updated_blocks,
    )


def _get_context_block(mrkdwn: str):
    return {
        "type": "context",
        "elements": [
            {
                "type": "mrkdwn",
                "text": mrkdwn,
            },
        ],
    }


def _parse_inputs(inputs: dict) -> Tuple[str, str, str, str]:
    manager = inputs["manager"]
    employee = inputs["employee"]
    start_date = datetime.fromtimestamp(inputs["start_date"]).strftime("%m/%d/%Y %H:%M")
    end_date = datetime.fromtimestamp(inputs["end_date"]).strftime("%m/%d/%Y %H:%M")
    return tuple(manager, employee, start_date, end_date)
