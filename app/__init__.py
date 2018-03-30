# -*- coding: utf-8 -*-


from flask import Flask, Response, jsonify

from app.model.mysql import *
from config import config

# print('default')
# print(config.config['default'])

# dbManager = MysqlManager(db=config.Config.mysql_db, user=config.Config.mysql_user,
#                          passwd=config.Config.mysql_passwd, host=config.Config.mysql_host,
#                          port=config.Config.mysql_port)

dbManager = MysqlManager()

class MyResponse(Response):
    @classmethod
    def force_type(cls, response, environ=None):
        if isinstance(response, (list, dict)):
            response = jsonify(response)
        return super(Response, cls).force_type(response, environ)


def create_app(config_name):
    app = Flask(__name__)
    app.response_class = MyResponse
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    dbManager.init_app(app)

    #print(app.config)

    from .api_1_0 import api as api_1_0_blueprint

    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    return app
