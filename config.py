class Config(object):
    TESTING = False
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'jonjc22@gmail.com'

class Production(Config):
    DEBUG = True
    MAIL_PASSWORD = 'jotakarratu'

class Development(Config):
    DEBUG = True
    MAIL_PASSWORD = 'brem zeca tivu czzt'
        
class Testing(Config):
    TESTING = True