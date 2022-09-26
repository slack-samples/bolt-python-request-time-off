from logging import Logger

from slack_sdk import WebClient
from slack_bolt import Complete, Ack

from .utils import get_context_block, update_request_message
from ..utils import parse_inputs


def approve_action(ack: Ack, client: WebClient, body: dict, complete: Complete, logger: Logger):
    try:
        ack()
        manager, employee, start_date, end_date = parse_inputs(body["function_data"]["inputs"])
        markdown = (
            f":white_check_mark: Time-off request for _{start_date}_ :arrow_right: "
            f"_{end_date}_ approved by <@{manager}>"
        )
        context_block = get_context_block(markdown)
        client.chat_postMessage(channel=employee, text=markdown, blocks=[context_block])

        update_request_message(client, body, context_block, markdown)
        complete()
    except Exception as e:
        logger.error(e)
        complete(error="Cannot approve request")
        raise e
