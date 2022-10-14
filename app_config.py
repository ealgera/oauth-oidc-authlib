import os
from dotenv import load_dotenv

### Azure App reg voor: python-auth-code-02
load_dotenv(".env")

# App Secrets
AAD_CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
if not AAD_CLIENT_SECRET:
    raise ValueError("CLIENT_SECRET is niet gedefinieerd!")

AAD_CLIENT_ID     = "73de801a-937d-4ee3-ba3e-dec460e1428b"     # Application (client) ID of app registration
AAD_TENANT_ID     = "121d18b6-96bd-4da0-9bb8-845d80a1ec21"
# In a production app, we recommend you use a more secure method of storing your secret,
# like Azure Key Vault. Or, use an environment variable as described in Flask's documentation:
# https://flask.palletsprojects.com/en/1.1.x/config/#configuring-from-environment-variables
# CLIENT_SECRET = os.getenv("CLIENT_SECRET")
# if not CLIENT_SECRET:
#     raise ValueError("Need to define CLIENT_SECRET environment variable")

AAD_AUTHORIZE_URL    = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"  # For multi-tenant app
AAD_ACCESS_TOKEN_URL = "https://login.microsoftonline.com/common/oauth2/v2.0/token" # Access Token endpoint for OAuth 1 and OAuth 2
AAD_AUTHORITY        = "https://login.microsoftonline.com/common"  # For multi-tenant app
# AUTHORITY = "https://login.microsoftonline.com/Enter_the_Tenant_Name_Here"

REDIRECT_PATH = "/getAToken"  # Used for forming an absolute URL to your redirect URI.
                              # The absolute URL must match the redirect URI you set
                              # in the app's registration in the Azure portal.

GRAPH_API_BASE = "https://graph.microsoft.com"

# You can find more Microsoft Graph API endpoints from Graph Explorer
# https://developer.microsoft.com/en-us/graph/graph-explorer
ENDPOINT = 'https://graph.microsoft.com/v1.0/users'  # This resource requires no admin consent

# You can find the proper permission names from this document
# https://docs.microsoft.com/en-us/graph/permissions-reference
SCOPE = "User.Read openid profile"

SESSION_TYPE = "filesystem"  # Specifies the token cache should be stored in server-side session