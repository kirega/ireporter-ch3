class Config():
    DEBUG = False
    TESTING = False
    
class DevelopmentConfig(Config):
    DEBUG = True
    ENV = "development"

class TestingConfig(Config):
    TESTING = True

settings = {
    'development': DevelopmentConfig,
    'testing':TestingConfig
}