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


#############################################################################################################

#twilio
# Your Account SID from twilio.com/console

# this upgraded SID for user
TWLIO_ACCOUNT_SID_UPGRADED_FOR_USER = "ACe211524106753eb639d9fae6ebd35bb2"

# this non upgrade SID for admin
TWLIO_ACCOUNT_SID_NONE_UPGRADED_FOR_ADMIN = "ACe335c5f83a4c6a3dc22f25cb5fe3d74d"


# Your Auth Token from twilio.com/console

# this upgraded auth_token for user
TWLIO_AUTH_TOKEN_UPGRADED_FOR_USER = "2d7c15d4df5846d341c3a67a7fec9b9b"

# this none upgraded auth_token for admin
TWLIO_AUTH_TOKEN_NONE_UPGRADED_FOR_ADMIN = "98f8f99a6bcbe14e0f5b9ab50ae55a31"

#############################################################################################################