from slackclient import SlackClient
from models import Message
from database import db
slack_write_token = "xoxp-2314941267-411607771605-593540160231-8033a3590a222c165da8d64439180880"
slack_read_token = "xoxb-2314941267-583747499857-JkH90GZCEz5XQnICe1RKrOio"
client_write = SlackClient(slack_write_token)
client_read = SlackClient(slack_read_token)
randomId = "C0298TP85"
botTestId = "C0C9V4Q82"
# list = client_read.api_call(
#     "channels.list"
# )
#
# for channel in list['channels']:
#     print(channel)


def download_messages(cursor=""):
    return client_write.api_call(
        "conversations.history",
        channel=randomId,
        limit=200,
        cursor=cursor
    )


def save_messages(raw_messages = []):
    for message in list(filter(lambda x: len(x['text']) > 0 and 'client_msg_id' in x.keys(), raw_messages)):
        found_message = db.query(Message).filter(Message.text == message['text']).first()
        if found_message is not None:
            new_message = Message(message['text'], message['client_msg_id'])
            db.add(new_message)
    db.commit()


def download_random_messages():
    curs = ""
    stop = False
    for num in range(1, 100):
        if stop:
            break
        response = download_messages(curs)
        save_messages(response["messages"])
        if "response_metadata" in response.keys() and "next_cursor" in response["response_metadata"]:
            curs = response["response_metadata"]["next_cursor"]
            print(curs)
        else:
            stop = True

    print('Closing')
    db.close()


def get_latest_message_from_channel(channel_id=randomId):
    return client_write.api_call(
        "conversations.history",
        channel=channel_id,
        limit=1
    )


def post_message_test(message=""):
    latest = get_latest_message_from_channel(botTestId)['messages'][0]
    latest_ts = latest['ts']
    return client_write.api_call(
        "chat.postMessage",
        channel=botTestId,
        text=message,
        thread_ts=latest_ts
    )


def post_message(message=""):
    latest = get_latest_message_from_channel(randomId)['messages'][0]
    latest_ts = latest['ts']
    return client_write.api_call(
        "chat.postMessage",
        channel=randomId,
        text=message,
        thread_ts=latest_ts
    )
