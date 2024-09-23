import os

# The allowed translation for you app
LANGUAGES = {
    "en": {"flag": "us", "name": "English"},
    #"es": {"flag": "es", "name": "Spanish"},
    #"it": {"flag": "it", "name": "Italian"},
    "fr": {"flag": "fr", "name": "French"},
    #"zh": {"flag": "cn", "name": "Chinese"},
    #"ja": {"flag": "jp", "name": "Japanese"},
    #"de": {"flag": "de", "name": "German"},
    #"pt": {"flag": "pt", "name": "Portuguese"},
    #"pt_BR": {"flag": "br", "name": "Brazilian Portuguese"},
    #"ru": {"flag": "ru", "name": "Russian"},
    #"ko": {"flag": "kr", "name": "Korean"},
    #"sk": {"flag": "sk", "name": "Slovak"},
    #"sl": {"flag": "si", "name": "Slovenian"},
}

ENABLE_PROXY_FIX = True

SECRET_KEY = os.getenv("SECRET_KEY", 'ChangeThisKeyPlease')

#---------------------------KEYCLOACK ----------------------------
# See: https://github.com/apache/superset/discussions/13915
# See: https://stackoverflow.com/questions/54010314/using-keycloakopenid-connect-with-apache-superset/54024394#54024394

from keycloak_security_manager  import  OIDCSecurityManager
from flask_appbuilder.security.manager import AUTH_OID

OIDC_ENABLE = os.getenv("OIDC_ENABLE", 'False')

if OIDC_ENABLE == 'True':
    AUTH_TYPE = AUTH_OID
    CUSTOM_SECURITY_MANAGER = OIDCSecurityManager
    # See: https://flask-oidc.readthedocs.io/en/latest/#flask_oidc.OpenIDConnect.require_login
    OIDC_CLIENT_SECRETS = os.getenv("OIDC_CLIENT_SECRETS", '/app/pythonpath/client_secret.json')
    OIDC_COOKIE_SECURE = True
    OIDC_REQUIRE_VERIFIED_EMAIL = False
    OIDC_OPENID_REALM = os.getenv("OIDC_OPENID_REALM")
    OIDC_INTROSPECTION_AUTH_METHOD = 'client_secret_post'
#--------------------------------------------------------------

APP_NAME = os.getenv("APP_NAME", 'DataViz')
APP_ICON = os.getenv("APP_ICON", '/static/assets/images/cf-logo.png')
APP_ICON_WIDTH = os.getenv("APP_ICON_WIDTH", 26)
LOGO_TOOLTIP = os.getenv("LOGO_TOOLTIP", 'DataViz by ComputableFacts')
LOGO_RIGHT_TEXT = os.getenv("LOGO_RIGHT_TEXT", 'DataViz')

FAVICONS = [{"href": os.getenv("APP_FAVICON", '/static/assets/images/cf-logo.png')}]


#--------------------------------------------------------------
# Alert & Report
# Changes to allow selenium to work with OIDC auth
# See: https://github.com/apache/superset/issues/14330#issuecomment-885656343
from superset.utils.urls import headless_url
from superset.utils.machine_auth import MachineAuthProvider

def auth_driver(driver, user):
    # Setting cookies requires doing a request first, but /login is redirected to oauth provider, and stuck there.
    driver.get(headless_url("/doesnotexist"))

    cookies = MachineAuthProvider.get_auth_cookies(user)

    for cookie_name, cookie_val in cookies.items():
        driver.add_cookie(dict(name=cookie_name, value=cookie_val))

    return driver

# Change the driver only for OIDC
if OIDC_ENABLE == 'True':
    WEBDRIVER_AUTH_FUNC = auth_driver
#--------------------------------------------------------------
# Alert & Report
# Send email

EMAIL_NOTIFICATIONS = os.getenv("EMAIL_NOTIFICATIONS", 'False')

if EMAIL_NOTIFICATIONS == 'True':

    EMAIL_NOTIFICATIONS = True
    EMAIL_REPORTS_SUBJECT_PREFIX = os.getenv("EMAIL_REPORTS_SUBJECT_PREFIX", '')

    ALERT_REPORTS_NOTIFICATION_DRY_RUN = False


    WEBDRIVER_BASEURL_USER_FRIENDLY = os.getenv("WEBDRIVER_BASEURL_USER_FRIENDLY", "http://localhost:8088/")

    SMTP_HOST = os.getenv("SMTP_HOST", 'smtp.sendgrid.net')
    SMTP_STARTTLS = True
    SMTP_SSL = False
    SMTP_USER = os.getenv("SMTP_USER", 'user')
    SMTP_PORT = os.getenv("SMTP_PORT", 587)
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", 'change_it')
    SMTP_MAIL_FROM = os.getenv("SMTP_MAIL_FROM", 'superset@superset.com')

# Deprecated ENABLE_SCHEDULED_EMAIL_REPORTS = True (WARNING:root:ENABLE_SCHEDULED_EMAIL_REPORTS is deprecated and will be removed in version 2.0.0)
# Deprecated in 1.2.0: ENABLE_ALERTS, SCHEDULED_EMAIL_DEBUG_MODE, EMAIL_REPORTS_CRON_RESOLUTION, EMAIL_ASYNC_TIME_LIMIT_SEC, EMAIL_REPORT_BCC_ADDRESS, EMAIL_REPORTS_USER

# Time before selenium times out after trying to locate an element on the page and wait
# for that element to load for a screenshot.
SCREENSHOT_LOCATE_WAIT = int(os.getenv("SCREENSHOT_LOCATE_WAIT", 10))
# Time before selenium times out after waiting for all DOM class elements named
# "loading" are gone.
SCREENSHOT_LOAD_WAIT = int(os.getenv("SCREENSHOT_LOAD_WAIT", 60))
# Selenium destroy retries
SCREENSHOT_SELENIUM_RETRIES = int(os.getenv("SCREENSHOT_SELENIUM_RETRIES", 5))
# Give selenium an headstart, in seconds
SCREENSHOT_SELENIUM_HEADSTART = int(os.getenv("SCREENSHOT_SELENIUM_HEADSTART", 3))
# Wait for the chart animation, in seconds
SCREENSHOT_SELENIUM_ANIMATION_WAIT = int(os.getenv("SCREENSHOT_SELENIUM_ANIMATION_WAIT", 5))

#--------------------------------------------------------------
