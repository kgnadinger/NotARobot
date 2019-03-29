from database import db
from models import Message
import markovify
from slack_client import post_message, botTestId


def sentence_generator():
    text = ""

    messages = db.query(Message).all()
    for message in messages:
        text += message.text + "\n"

    text_model = markovify.Text(text)

    return text_model.make_sentence()


def post_real_message():
    return post_message(sentence_generator(), channel=botTestId)

post_real_message()