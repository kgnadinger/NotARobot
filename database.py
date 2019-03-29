import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def connect(user, password, db, host="localhost", port=5432):
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)

    con = sqlalchemy.create_engine(url, client_encoding='utf8')
    return con


engine = connect('kevingnadinger', '', 'not_a_robot_dev')
Base = declarative_base()
Session = sessionmaker(bind=engine)
db = Session()
