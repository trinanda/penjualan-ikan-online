DEBUG = True

SQLALCHEMY_DATABASE_URI = 'postgresql://irwan:12345@service_postgresql_docker/jualikan'
DATABASE_FILE = SQLALCHEMY_DATABASE_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True


SECRET_KEY = '12345'

# Flask-Security config
SECURITY_URL_PREFIX = "/admin"
SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
SECURITY_PASSWORD_SALT = "ATGUOHAELKiubahiughaerGOJAEGj"

# Flask-Security URLs, overridden because they don't put a / at the end
SECURITY_LOGIN_URL = "/login/"
SECURITY_LOGOUT_URL = "/logout/"
SECURITY_REGISTER_URL = "/register/"

SECURITY_POST_LOGIN_VIEW = "/admin/"
SECURITY_POST_LOGOUT_VIEW = "/admin/"
SECURITY_POST_REGISTER_VIEW = "/admin/"

# Flask-Security features
SECURITY_REGISTERABLE = True
SECURITY_SEND_REGISTER_EMAIL = False

#############################################################################################################
UPLOADED_PHOTOS_DEST = 'web_app/files/'
#############################################################################################################

#############################################################################################################
## Adding reCAPTCHA to your site
# https://www.google.com/recaptcha/admin#site/341690749?setup
# Site key
RECAPTCHA_PUBLIC_KEY = '6Ld9yV0UAAAAAO80R7BhJYQij2t4yXAbbEiZbFFW'
# Secret key
RECAPTCHA_PRIVATE_KEY = '6Ld9yV0UAAAAAHMETUy4xdllS-FS4LLFDBC6j5F2'
TESTING = False
RECAPTCHA_SIZE = "square"
RECAPTCHA_RTABINDEX = 10
RECAPTCHA_THEME = "dark"
RECAPTCHA_ENABLED = True

#############################################################################################################