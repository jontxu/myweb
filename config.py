class Config(object):
    TESTING = False
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'jonjc22@gmail.com'

class Production(Config):
    DEBUG = False
    MAIL_PASSWORD = 'jotakarratu'

class Development(Config):
    DEBUG = False
    MAIL_PASSWORD = 'lol'
        
class Testing(Config):
    TESTING = True