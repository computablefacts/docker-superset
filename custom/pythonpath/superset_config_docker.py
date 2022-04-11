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

#    AUTH_USER_REGISTRATION = True
#    AUTH_USER_REGISTRATION_ROLE = get_env_variable("AUTH_USER_REGISTRATION_ROLE", 'Public')
#--------------------------------------------------------------
