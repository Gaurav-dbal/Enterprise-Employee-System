import requests


# ===========================================
# API Configuration
# ===========================================

BASE_URL = "https://jsonplaceholder.typicode.com"

API_KEY = "my-secret-api-key"


# ===========================================
# Authentication Function
# ===========================================

def authenticate():

    print("\n========== API Authentication ==========")

    user_api_key = input("Enter API Key : ")

    if user_api_key == API_KEY:

        print("\nAuthentication Successful.")
        return True

    else:

        print("\nAuthentication Failed.")
        print("Status Code : 401")
        return False


# ===========================================
# Create Headers
# ===========================================

def create_headers():

    token = input("Enter Bearer Token : ")

    headers = {

        "Authorization": f"Bearer {token}",

        "Content-Type": "application/json"

    }

    return headers


# ===========================================
# Get Users
# ===========================================

def get_users(headers):

    print("\n========== GET USERS ==========")

    url = f"{BASE_URL}/users"

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        print(f"Status Code : {response.status_code}")

        if response.status_code == 200:

            users = response.json()

            print("\nID | Name | Email")
            print("-" * 70)

            for user in users:

                print(
                    f"{user['id']} | "
                    f"{user['name']} | "
                    f"{user['email']}"
                )

        elif response.status_code == 401:

            print("Unauthorized.")
            print("Invalid authentication credentials.")

        elif response.status_code == 403:

            print("Forbidden.")
            print("You don't have permission.")

        else:

            print("API request failed.")

    except requests.exceptions.RequestException as error:

        print("\nAPI Connection Failed.")
        print(f"Error : {error}")


# ===========================================
# Main Program
# ===========================================

print("\n==========================================")
print("       Enterprise API Authentication")
print("==========================================")

if authenticate():

    headers = create_headers()

    print("\nAuthentication information prepared.")

    get_users(headers)

else:

    print("\nAccess Denied.")
    print("Application stopped.")