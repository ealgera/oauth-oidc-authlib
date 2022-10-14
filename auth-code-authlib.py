import json
import requests
from flask import Flask, redirect, url_for, render_template, session, request
from flask_session import Session # # Voor server-side Session. Session wordt niet direct gebruikt maar via flask.session
from authlib.integrations.flask_client import OAuth

import app_config

app = Flask(__name__)
app.config.from_object(app_config)
Session(app)

client = OAuth(app)


@app.route("/")
def index():

    if not session.get("tokens"):            # Geen 'tokens' in de sessie, dan eerst aanmelden via de /login route
        client.register(
            name            = 'azure_ad',
            client_id       = app_config.AAD_CLIENT_ID,
            client_secret   = app_config.AAD_CLIENT_SECRET,
            access_token_url= app_config.AAD_ACCESS_TOKEN_URL,
            access_token_params=None,
            authorize_url   = app_config.AAD_AUTHORIZE_URL,
            authorize_params= None,
            api_base_url    = app_config.GRAPH_API_BASE,
            client_kwargs   = {
                'scope': app_config.SCOPE
            },
            server_metadata_url=f"https://login.microsoftonline.com/common/v2.0/.well-known/openid-configuration",
        )

        return redirect(url_for("login"))

    return render_template(
        "index.html",
        user=session["tokens"],
        my_session=session,
        app_id=app_config.AAD_CLIENT_ID,
        app_secret=app_config.AAD_CLIENT_SECRET
    )

@app.route("/login")
def login():
    '''
    '''
    azure_ad = client.create_client("azure_ad")
    # print(f"[info] <login> AZURE_AD Client: {type(azure_ad)}")
    
    # for k, v in vars(azure_ad).items():
    #     print(f"[info] <login> {k}: {v}")

    redirect_uri = "http://localhost:5000" + app_config.REDIRECT_PATH  # url_for(app_config.REDIRECT_PATH)

    auth_uri = azure_ad.authorize_redirect(redirect_uri)
    auth_url = vars(auth_uri).get('headers').get('Location')

    # return azure_ad.authorize_redirect(redirect_uri)

    return render_template(
        "login.html", 
        auth_url=auth_url,
        app_id=app_config.AAD_CLIENT_ID,
        app_secret=app_config.AAD_CLIENT_SECRET,
        auth_info = vars(auth_uri)
    )

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        app_config.AAD_AUTHORITY + "/oauth2/v2.0/logout" +
        "?post_logout_redirect_uri=" + url_for("index", _external=True)
    )

@app.route(app_config.REDIRECT_PATH)  # Leidt naar: /getAToken
def authorized():
    '''
    !!! Issuer validatie in /authlib/jose/rfc7519/claims.py uitgezet in functie _validate_claim_value. 
    Zie ook: https://github.com/MicrosoftDocs/azure-docs/issues/38427 en: https://login.microsoftonline.com/common/v2.0/.well-known/openid-configuration
    MS geeft als 'issuer' aan: "https://login.microsoftonline.com/{tenantid}/v2.0". Dit is niet volgens de OIDC rfc.
    De code vergelijkt "https://login.microsoftonline.com/<werkelijk id>/v2.0" met "https://login.microsoftonline.com/{tenantid}/v2.0"
    Deze vergelijking klopt niet en er volgt een InvalidClaimError, invalid_claim: Invalid claim "iss"
    '''
    print(f"[info] <Authorized> ...")

    try:
        token = client.azure_ad.authorize_access_token()
        session["tokens"] = token
    except Exception as e:
        print(f"\n *** FOUT ***")
        print(e)
        print()

    for token_key, token_value in token.items():
        print(f"[info] -- item {token_key} : {token_value}")

    # return redirect(url_for("logout"))
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run()
