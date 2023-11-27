class Config:
    # General configuration
    SECRET_KEY = 'to_fill_at_release'

class DevelopementConfig(Config):
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'trafico'
    MYSQL_PASSWORD = 'trafico.1234'
    MYSQL_DB = 'datos_abiertos'
    MYSQL_CURSORCLASS = 'DictCursor'
    SQLALCHEMY_DATABASE_URI = f'mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:3306/{MYSQL_DB}'


config = {
    'dev': DevelopementConfig
}