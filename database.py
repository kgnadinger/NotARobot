import os
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from configparser import ConfigParser


def build_db_conn_string(cfg):
    if cfg.get("database", "system").lower() == "sqlite":
        return "{system}:///{db}".format(**{
            "system": cfg.get("database", "system"),
            "db": cfg.get("database", "database"),
        })

    return "{system}://{username}:{password}@{host}/{db}".format(**{
        "system": cfg.get("database", "system"),
        "username": cfg.get("database", "username"),
        "password": cfg.get("database", "password"),
        "host": cfg.get("database", "host"),
        "db": cfg.get("database", "database"),
    })

cfg_file = ConfigParser()
path_to_cfg = os.path.dirname(__file__)
path_to_cfg = os.path.join(path_to_cfg, "robot_env.cfg")
cfg_file.read(path_to_cfg)


engine = sqlalchemy.create_engine(build_db_conn_string(cfg_file))
Base = declarative_base()
Session = sessionmaker(bind=engine)
db = Session()
