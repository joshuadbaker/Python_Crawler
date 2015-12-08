import os

class Config(object):
  DEBUG = False
  TESTING = False
  CSRF_ENABLED = True
  SECRET_KEY = "needs-to-be-changed"
  SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

# class ProductionConfig(Config):
#   DEBUG = False

# class StageConfig(Config):
#   DEVELOPMENT = True
#   DEBUG = True

class DevelopmentConfig(Config):
  DEVELOPMENT = True
  DEBUG = True

# class TestingConfig(Config):
#   TESTING = True

# print(os.environ['DATABASE_URL'])