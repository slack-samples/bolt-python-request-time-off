from slack_sdk import WebClient


def update_request_message(client: WebClient, body: dict, block: dict, text: str):
    updated_blocks = body["message"]["blocks"][:-1]
    updated_blocks.append(block)

    client.chat_update(
        channel=body["container"]["channel_id"],
        ts=body["container"]["message_ts"],
        text=text,
        blocks=updated_blocks,
    )


def get_context_block(markdown: str) -> dict:
    return {
        "type": "context",
        "elements": [
            {
                "type": "mrkdwn",
                "text": markdown,
            },
        ],
    }
