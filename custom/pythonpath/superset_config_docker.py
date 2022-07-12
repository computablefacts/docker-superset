import os
from typing import Optional

def get_env_variable(var_name: str, default: Optional[str] = None) -> str:
    """Get the environment variable or raise exception."""
    try:
        return os.environ[var_name]
    except KeyError:
        if default is not None:
            return default
        else:
            error_msg = "The environment variable {} was missing, abort...".format(
                var_name
            )
            raise EnvironmentError(error_msg)


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

SECRET_KEY = get_env_variable("SECRET_KEY", 'ChangeThisKeyPlease')

#---------------------------KEYCLOACK ----------------------------
# See: https://github.com/apache/superset/discussions/13915
# See: https://stackoverflow.com/questions/54010314/using-keycloakopenid-connect-with-apache-superset/54024394#54024394

from keycloak_security_manager  import  OIDCSecurityManager
from flask_appbuilder.security.manager import AUTH_OID

OIDC_ENABLE = get_env_variable("OIDC_ENABLE", 'False')

if OIDC_ENABLE == 'True':
    AUTH_TYPE = AUTH_OID
    CUSTOM_SECURITY_MANAGER = OIDCSecurityManager
    # See: https://flask-oidc.readthedocs.io/en/latest/#flask_oidc.OpenIDConnect.require_login
    OIDC_CLIENT_SECRETS = get_env_variable("OIDC_CLIENT_SECRETS", '/app/pythonpath/client_secret.json')
    OIDC_COOKIE_SECURE = True
    OIDC_REQUIRE_VERIFIED_EMAIL = False
    OIDC_OPENID_REALM = get_env_variable("OIDC_OPENID_REALM")
    OIDC_INTROSPECTION_AUTH_METHOD = 'client_secret_post'
#--------------------------------------------------------------

APP_NAME = get_env_variable("APP_NAME", 'DataViz')
APP_ICON = get_env_variable("APP_ICON", '/static/assets/images/cf-logo.png')
APP_ICON_WIDTH = get_env_variable("APP_ICON_WIDTH", 26)
LOGO_TOOLTIP = get_env_variable("LOGO_TOOLTIP", 'DataViz by ComputableFacts')
LOGO_RIGHT_TEXT = get_env_variable("LOGO_RIGHT_TEXT", 'DataViz')

FAVICONS = [{"href": get_env_variable("APP_FAVICON", '/static/assets/images/cf-logo.png')}]


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

# TODO: check if it still works when OIDC is disable
WEBDRIVER_AUTH_FUNC = auth_driver
#--------------------------------------------------------------
# Alert & Report
# Send email

EMAIL_NOTIFICATIONS = get_env_variable("EMAIL_NOTIFICATIONS", 'False')

if EMAIL_NOTIFICATIONS == 'True':

    EMAIL_NOTIFICATIONS = True
    EMAIL_REPORTS_SUBJECT_PREFIX = get_env_variable("EMAIL_REPORTS_SUBJECT_PREFIX", '[DataViz Report] ')

    ALERT_REPORTS_NOTIFICATION_DRY_RUN = False


    WEBDRIVER_BASEURL_USER_FRIENDLY = get_env_variable("WEBDRIVER_BASEURL_USER_FRIENDLY", "http://localhost:8088/")

    SMTP_HOST = get_env_variable("SMTP_HOST", 'smtp.sendgrid.net')
    SMTP_STARTTLS = True
    SMTP_SSL = False
    SMTP_USER = get_env_variable("SMTP_USER", 'user')
    SMTP_PORT = get_env_variable("SMTP_PORT", 587)
    SMTP_PASSWORD = get_env_variable("SMTP_PASSWORD", 'change_it')
    SMTP_MAIL_FROM = get_env_variable("SMTP_MAIL_FROM", 'superset@superset.com')

# Deprecated ENABLE_SCHEDULED_EMAIL_REPORTS = True (WARNING:root:ENABLE_SCHEDULED_EMAIL_REPORTS is deprecated and will be removed in version 2.0.0)
# Deprecated in 1.2.0: ENABLE_ALERTS, SCHEDULED_EMAIL_DEBUG_MODE, EMAIL_REPORTS_CRON_RESOLUTION, EMAIL_ASYNC_TIME_LIMIT_SEC, EMAIL_REPORT_BCC_ADDRESS, EMAIL_REPORTS_USER

# Time before selenium times out after trying to locate an element on the page and wait
# for that element to load for a screenshot.
SCREENSHOT_LOCATE_WAIT = 33
# Time before selenium times out after waiting for all DOM class elements named
# "loading" are gone.
SCREENSHOT_LOAD_WAIT = 187
# Selenium destroy retries
SCREENSHOT_SELENIUM_RETRIES = 5
# Give selenium an headstart, in seconds
SCREENSHOT_SELENIUM_HEADSTART = 3
# Wait for the chart animation, in seconds
SCREENSHOT_SELENIUM_ANIMATION_WAIT = 5

#--------------------------------------------------------------
