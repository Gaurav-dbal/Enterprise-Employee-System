import requests


# ===========================================
# API Configuration
# ===========================================

BASE_URL = "https://jsonplaceholder.typicode.com"


# ===========================================
# Helper Function
# ===========================================

def check_response(response):

    print(f"Status Code : {response.status_code}")

    if response.status_code in [200, 201]:
        return True

    elif response.status_code == 400:
        print("Bad Request.")
        print("Please check the data you sent.")

    elif response.status_code == 401:
        print("Unauthorized.")
        print("Authentication is required.")

    elif response.status_code == 403:
        print("Forbidden.")
        print("You don't have permission.")

    elif response.status_code == 404:
        print("Resource Not Found.")

    elif response.status_code == 500:
        print("Internal Server Error.")

    else:
        print("Unexpected API response.")

    return False


# ===========================================
# CREATE - POST
# ===========================================

def create_user():

    print("\n========== CREATE USER ==========")

    name = input("Enter Name       : ")
    email = input("Enter Email      : ")
    department = input("Enter Department : ")

    user_data = {

        "title": department,
        "body": name,
        "email": email,
        "userId": 1

    }

    url = f"{BASE_URL}/posts"

    try:

        response = requests.post(
            url,
            json=user_data,
            timeout=10
        )

        if check_response(response):

            created_user = response.json()

            print("\nUser Created Successfully.")

            print(f"ID         : {created_user.get('id')}")
            print(f"Name       : {created_user.get('body')}")
            print(f"Department : {created_user.get('title')}")

    except requests.exceptions.RequestException as error:

        print("\nAPI Connection Failed.")
        print(f"Error : {error}")


# ===========================================
# READ - GET ALL
# ===========================================

def get_users():

    print("\n========== VIEW USERS ==========")

    url = f"{BASE_URL}/users"

    try:

        response = requests.get(
            url,
            timeout=10
        )

        if check_response(response):

            users = response.json()

            print("\nID | Name | Email | Company | City")
            print("-" * 100)

            for user in users:

                print(
                    f"{user['id']} | "
                    f"{user['name']} | "
                    f"{user['email']} | "
                    f"{user['company']['name']} | "
                    f"{user['address']['city']}"
                )

    except requests.exceptions.RequestException as error:

        print("\nAPI Connection Failed.")
        print(f"Error : {error}")


# ===========================================
# READ - GET ONE
# ===========================================

def search_user():

    print("\n========== SEARCH USER ==========")

    user_id = input("Enter User ID : ")

    url = f"{BASE_URL}/users/{user_id}"

    try:

        response = requests.get(
            url,
            timeout=10
        )

        if check_response(response):

            user = response.json()

            print("\n========== User Details ==========")

            print(f"ID          : {user['id']}")
            print(f"Name        : {user['name']}")
            print(f"Username    : {user['username']}")
            print(f"Email       : {user['email']}")
            print(f"Company     : {user['company']['name']}")
            print(f"City        : {user['address']['city']}")
            print(f"Latitude    : {user['address']['geo']['lat']}")
            print(f"Longitude   : {user['address']['geo']['lng']}")

    except requests.exceptions.RequestException as error:

        print("\nAPI Connection Failed.")
        print(f"Error : {error}")


# ===========================================
# UPDATE - PUT
# ===========================================

def update_user():

    print("\n========== UPDATE USER ==========")

    user_id = input("Enter User ID : ")

    name = input("Enter New Name       : ")
    email = input("Enter New Email      : ")
    department = input("Enter New Department : ")

    updated_data = {

        "id": int(user_id),
        "title": department,
        "body": name,
        "email": email,
        "userId": 1

    }

    url = f"{BASE_URL}/posts/{user_id}"

    try:

        response = requests.put(
            url,
            json=updated_data,
            timeout=10
        )

        if check_response(response):

            updated_user = response.json()

            print("\nUser Updated Successfully.")

            print(f"ID         : {updated_user.get('id')}")
            print(f"Name       : {updated_user.get('body')}")
            print(f"Department : {updated_user.get('title')}")
            print(f"Email      : {updated_user.get('email')}")

    except requests.exceptions.RequestException as error:

        print("\nAPI Connection Failed.")
        print(f"Error : {error}")


# ===========================================
# DELETE
# ===========================================

def delete_user():

    print("\n========== DELETE USER ==========")

    user_id = input("Enter User ID : ")

    url = f"{BASE_URL}/posts/{user_id}"

    try:

        response = requests.delete(
            url,
            timeout=10
        )

        if check_response(response):

            print("\nUser Deleted Successfully.")

    except requests.exceptions.RequestException as error:

        print("\nAPI Connection Failed.")
        print(f"Error : {error}")


# ===========================================
# MAIN MENU
# ===========================================

while True:

    print("\n==========================================")
    print("          Enterprise API CRUD")
    print("==========================================")

    print("1. Create User")
    print("2. View All Users")
    print("3. Search User")
    print("4. Update User")
    print("5. Delete User")
    print("6. Exit")

    choice = input("\nEnter your choice : ")

    if choice == "1":

        create_user()

    elif choice == "2":

        get_users()

    elif choice == "3":

        search_user()

    elif choice == "4":

        update_user()

    elif choice == "5":

        delete_user()

    elif choice == "6":

        print("\nThank you for using Enterprise API CRUD.")
        break

    else:

        print("\nInvalid Choice.")