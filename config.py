class Config(object):
    SECRET_KEY = 'marvakh-secret-key'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://root:root@localhost/auto_inspection'
    SQLALCHEMY_TRACK_MODIFICATIONS = False