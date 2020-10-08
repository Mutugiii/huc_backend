from decouple import config

class Config:
    '''
    Parent config class for all the child config classes
    '''
    SQLALCHEMY_DATABASE_URI = config('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProdConfig(Config):
    '''
    Class for Production configurations
    '''
    DEBUG=False

class TestConfig(Config):
    '''
    Class for testing configurations
    '''
    pass

class DevConfig(Config):
    '''
    Class for development configurations
    '''
    DEBUG=True

config_options = {
    'production': ProdConfig,
    'development': DevConfig,
    'testing': TestConfig
}
