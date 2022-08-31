from datetime import datetime
from logging import Logger

from slack_sdk import WebClient
from slack_bolt import Complete, Ack

from app import app

@app.function("review_approval")
def request_approval(event, client: WebClient, complete: Complete, logger: Logger):
    try:
        logger.info(f"my real token: {client.token}")
        inputs = event["inputs"]
        manager = inputs["manager"]
        employee = inputs["employee"]
        end_date = datetime.fromtimestamp(inputs["end_date"]).strftime("%m/%d/%Y %H:%M")
        start_date = datetime.fromtimestamp(inputs["start_date"]).strftime("%m/%d/%Y %H:%M")

        client.chat_postMessage(
            channel=manager,
            text='A new time-off request has been submitted.',
            blocks=[
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "A new time-off request has been submitted"
                    }
                },
                {
                    "type": 'section',
                    "text": {
                        "type": 'mrkdwn',
                        "text": f"*From: * <@{employee}>",
                    },
                },
                {
                    "type": 'section',
                    "text": {
                        "type": 'mrkdwn',
                        "text": f"*Dates: * _{start_date}_ :arrow_right: _{end_date}_",
                    },
                },
                {
                    "type": 'actions',
                    "block_id": 'approve-deny-buttons',
                    "elements": [
                        {
                            "type": 'button',
                            "text": {
                                "type": 'plain_text',
                                "text": 'Approve',
                            },
                            "action_id": 'approve_action_id',
                            "style": 'primary',
                        },
                        {
                            "type": 'button',
                            "text": {
                                "type": 'plain_text',
                                "text": 'Deny',
                            },
                            "action_id": 'deny_action_id',
                            "style": 'danger',
                        }
                    ]
                }
            ])
    except Exception as e:
        logger.error(e)
        complete(error="Cannot request approval")
        raise e


@request_approval.action("approve_action_id")
def approve_action(ack: Ack, client: WebClient, body, complete: Complete, logger: Logger):
    try:
        ack()
        inputs = body["function_data"]["inputs"]
        manager = inputs["manager"]
        employee = inputs["employee"]
        end_date = datetime.fromtimestamp(inputs["end_date"]).strftime("%m/%d/%Y %H:%M")
        start_date = datetime.fromtimestamp(inputs["start_date"]).strftime("%m/%d/%Y %H:%M")

        context_block = get_context_block(start_date, end_date, manager)

        updated_blocks = body["message"]["blocks"][:-1]
        updated_blocks.append(context_block)

        text = f'Time-off request for {start_date} to {end_date} approved by <@{manager}>'

        client.chat_postMessage(
            channel=employee,
            text=text,
            blocks=[context_block])

        client.chat_update(
            channel=body["container"]["channel_id"],
            ts=body["container"]["message_ts"],
            text=text,
            blocks=updated_blocks
        )

        complete()
    except Exception as e:
        logger.error(e)
        complete("Cannot request approval")
        raise e


def get_context_block(start_date, end_date, manager):
    return {
        "type": 'context',
        "elements": [
            {
                "type": 'mrkdwn',
                "text": f":white_check_mark: Time-off request for _{start_date}_ :arrow_right: _{end_date}_ approved by <@{manager}>",
            },
        ],
    }

@request_approval.action("deny_action_id")
def deny_action(ack: Ack, client: WebClient, body, complete: Complete, logger: Logger):
    try:
        ack()
        inputs = body["function_data"]["inputs"]
        manager = inputs["manager"]
        employee = inputs["employee"]
        end_date = datetime.fromtimestamp(inputs["end_date"]).strftime("%m/%d/%Y %H:%M")
        start_date = datetime.fromtimestamp(inputs["start_date"]).strftime("%m/%d/%Y %H:%M")

        context_block = get_context_block(start_date, end_date, manager)

        updated_blocks = body["message"]["blocks"][:-1]
        updated_blocks.append(context_block)

        text = f"Time-off request for {end_date} to {start_date} denied by <@{manager}>"

        client.chat_postMessage(
            channel=employee,
            text=text,
            blocks=[context_block]
        )

        client.chat_update(
            channel=body["container"]["channel_id"],
            ts=body["container"]["message_ts"],
            text=text,
            blocks=updated_blocks
        )
        complete()
    except Exception as e:
        logger.error(e)
        complete(error="Cannot request approval")
        raise e


def get_context_block(start_date, end_date, manager):
    return {
        "type": 'context',
        "elements": [
            {
                "type": 'mrkdwn',
                "text": f":no_entry: Time-off request for _{start_date}_ :arrow_right: _{end_date}_ denied by <@{manager}>",
            },
        ],
    }
