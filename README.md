# oauth-example-flask
A test application to test the OAuth2/OIDC flow with Azure AD.
Conform the Authlib library and Python (3.x).

### Setup (Linux)
#### Python setup
- create a virtual Python environment with: python3 -m venv venv
- activate the virtual Python environment with: source venv/bin/activate
- install the needed Python libraries: pip install -r requirements.txt

#### App setup
- create in Azure AD a web-app registration.
- create an API permission (scope).
- copy the client secret and client id.
- create an .env file like the example file .env_example
- add the client secret to the .env file. Use the CLIENT_SECRET variable.
- change / set needed variables in app_config.py (in any case: CLIENT_ID and maybe SCOPE, see app_config.py)

#### Start the app
- start: python auth-code-authlib.py
- goto http://localhost:5000 in a browser

### !! Important !!
I've changed the code in /authlib/jose/rfc7519/claims.py, function _validate_claim_value.
I deactivated this function (commented) because Microsoft does not comply to the OIDC RFC, so there is no claim validation!
If you clone this code you should also 'patch' this code if you get an error like InvalidClaimError, invalid_claim: Invalid claim "iss".
(code in venv/lib/python<#>/site-packages/authlib/jose/rfc7519/claims.py)
The problem is that Microsoft shows the 'issuer' (iss) as: "https://login.microsoftonline.com/{tenantid}/v2.0" in '.well-known/openid-configuration'.
The claim will be compared against "https://login.microsoftonline.com/[real tenant-id]/v2.0" and willl fail.
