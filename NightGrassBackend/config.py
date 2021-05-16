
class BaseConfig:
    SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]flask_app/'
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite:///:memory:'


class DevelopmentConfig(BaseConfig):

    user = 'root'
    password = 'Txcug125'
    database = 'nightgrass_test'

    SQLALCHEMY_TRACK_MODIFICATIONS = True

    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@localhost:3306/{}'.format(user,password,database)
    SQLALCHEMY_POOL_SIZE = 30
    SQLALCHEMY_POOL_TIMEOUT = 30            # 30s
    SQLALCHEMY_POOL_RECYCLE = 60 * 60       # 1 hour
    SQLALCHEMY_ECHO = False


class TestingConfig(DevelopmentConfig):
    pass


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1:3306/flask_app'
    SQLALCHEMY_POOL_SIZE = 30
    SQLALCHEMY_POOL_TIMEOUT = 30            # 30s
    SQLALCHEMY_POOL_RECYCLE = 60 * 60       # 1 hour
    SQLALCHEMY_ECHO = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
