DEBUG = True

SQLALCHEMY_DATABASE_URI = 'postgresql//irwan:12345@service_postgresql_docker/jualikan'
DATABASE_FILE = SQLALCHEMY_DATABASE_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False


SECRET_KEY = '12345'