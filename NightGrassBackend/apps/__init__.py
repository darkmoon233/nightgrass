import os
from flask import Flask
from .NightGrassBackend import init_blue_print
from .utils import config_log
from NightGrassBackend.config import config
from flask_sqlalchemy import SQLAlchemy
import pymysql
from flask import g, current_app


def create_app():
    config_log()
    app = Flask(__name__)
    env = os.environ.get("FLASK_ENV", "default")
    app.config.from_object(config.get(env))
    app.logger.info("env{}".format(config.get(env)))

    db = SQLAlchemy(app)
    # 删除所有表
    db.drop_all()
    # 创建所有表
    db.create_all()

    init_blue_print(app)

    return app
