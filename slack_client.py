from slackclient import SlackClient
from models import Message
from database import db, cfg_file

slack_write_token = cfg_file.get("slack", "slack_write_token")
slack_read_token = cfg_file.get("slack", "slack_read_token")
client_write = SlackClient(slack_write_token)
client_read = SlackClient(slack_read_token)
randomId = "C0298TP85"
botTestId = "C0C9V4Q82"
quotesId = 'C0C1PA0D9'


def get_channel_list():
    channel_list = client_read.api_call(
        "channels.list"
    )

    channels = []
    for channel in channel_list['channels']:
        channels.append({'id': channel['id'], 'name': channel['name']})
    return channels


def get_channel_information(name):
    return list(filter(lambda x: x['name'] == name, get_channel_list()))


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


def post_message_test(message="", channel=botTestId):
    latest = get_latest_message_from_channel(botTestId)['messages'][0]
    latest_ts = latest['ts']
    return client_write.api_call(
        "chat.postMessage",
        channel=channel,
        text=message,
        thread_ts=latest_ts
    )


def post_message(message="", channel=randomId):
    latest = get_latest_message_from_channel(channel)['messages'][0]
    latest_ts = latest['ts']
    return client_write.api_call(
        "chat.postMessage",
        channel=channel,
        text=message,
        thread_ts=latest_ts
    )
