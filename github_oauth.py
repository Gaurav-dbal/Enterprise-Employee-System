import os
import secrets

import requests
from dotenv import load_dotenv
from flask import Flask, request, redirect


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# CONFIGURATION
# ============================================================

CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")

AUTHORIZE_URL = os.getenv("GITHUB_AUTHORIZE_URL")
TOKEN_URL = os.getenv("GITHUB_TOKEN_URL")
API_URL = os.getenv("GITHUB_API_URL")

CALLBACK_URL = os.getenv("GITHUB_CALLBACK_URL")


# ============================================================
# FLASK APPLICATION
# ============================================================

app = Flask(__name__)


# ============================================================
# SECURITY STATE
# ============================================================

oauth_state = secrets.token_urlsafe(32)


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    return """
    <h1>Enterprise OAuth Learning Application</h1>

    <p>
        <a href="/login">Login with GitHub</a>
    </p>
    """


# ============================================================
# LOGIN
# ============================================================

@app.route("/login")
def login():

    authorization_url = (

        f"{AUTHORIZE_URL}"

        f"?client_id={CLIENT_ID}"

        f"&redirect_uri={CALLBACK_URL}"

        f"&state={oauth_state}"

    )

    return redirect(authorization_url)


# ============================================================
# CALLBACK
# ============================================================

@app.route("/callback")
def callback():

    returned_state = request.args.get("state")

    code = request.args.get("code")

    # --------------------------------------------------------
    # Validate state
    # --------------------------------------------------------

    if returned_state != oauth_state:

        return "Invalid OAuth state.", 400

    # --------------------------------------------------------
    # Check authorization code
    # --------------------------------------------------------

    if not code:

        return "Authorization code missing.", 400

    print("\nAuthorization Code Received.")

    # --------------------------------------------------------
    # Exchange authorization code for access token
    # --------------------------------------------------------

    token_data = {

        "client_id": CLIENT_ID,

        "client_secret": CLIENT_SECRET,

        "code": code,

        "redirect_uri": CALLBACK_URL

    }

    headers = {

        "Accept": "application/json"

    }

    try:

        response = requests.post(

            TOKEN_URL,

            data=token_data,

            headers=headers,

            timeout=10

        )

        print(
            f"Token Endpoint Status : "
            f"{response.status_code}"
        )

        if response.status_code != 200:

            print(response.text)

            return "Failed to obtain access token.", 400

        token_response = response.json()

        access_token = token_response.get(
            "access_token"
        )

        if not access_token:

            return "Access token not received.", 400

        print("Access Token Received Successfully.")

        # ----------------------------------------------------
        # Call protected API
        # ----------------------------------------------------

        return get_github_user(access_token)

    except requests.exceptions.RequestException as error:

        print(f"Error : {error}")

        return "API connection failed.", 500


# ============================================================
# PROTECTED API
# ============================================================

def get_github_user(access_token):

    headers = {

        "Authorization": f"Bearer {access_token}",

        "Accept": "application/vnd.github+json"

    }

    try:

        response = requests.get(

            API_URL,

            headers=headers,

            timeout=10

        )

        print(
            f"GitHub API Status : "
            f"{response.status_code}"
        )

        if response.status_code == 200:

            user = response.json()

            return f"""
            <h1>Authentication Successful</h1>

            <h2>GitHub User</h2>

            <p><b>ID:</b> {user.get("id")}</p>

            <p><b>Login:</b> {user.get("login")}</p>

            <p><b>Name:</b> {user.get("name")}</p>

            <p><b>Company:</b> {user.get("company")}</p>

            <p><b>Public Repositories:</b>
            {user.get("public_repos")}</p>

            <h3>OAuth Flow Completed Successfully.</h3>
            """

        elif response.status_code == 401:

            return (
                "<h1>401 Unauthorized</h1>"
                "<p>Access token is invalid.</p>"
            ), 401

        elif response.status_code == 403:

            return (
                "<h1>403 Forbidden</h1>"
                "<p>Access is not permitted.</p>"
            ), 403

        else:

            return (
                f"API request failed: {response.text}",
                response.status_code
            )

    except requests.exceptions.RequestException as error:

        return (
            f"GitHub API connection failed: {error}",
            500
        )


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    print("\n==========================================")
    print("       GitHub OAuth 2.0 Learning App")
    print("==========================================")

    print("\nOpen in browser:")
    print("http://localhost:8000")

    app.run(
        host="localhost",
        port=8000,
        debug=True
    )