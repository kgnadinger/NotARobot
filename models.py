from sqlalchemy import Table, Column, Integer, String, ForeignKey, Text
from database import Base, engine


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    text = Column(Text)
    client_msg_id = Column(String)

    def __init__(self, text, client_msg_id):
        self.text = text
        self.client_msg_id = client_msg_id


Base.metadata.create_all(engine)
