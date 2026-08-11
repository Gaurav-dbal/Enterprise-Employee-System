import requests

url = "https://jsonplaceholder.typicode.com/users"

try:
    response = requests.get(url, timeout=10)
    response = requests.get(url)
    print(response)

except requests.exceptions.RequestException:

    print("API request failed.")

 

if response.status_code == 200:

    users = response.json()

    print("\n========== User List ==========")
    print("\n========== User Directory ==========")
    print("ID | Name | Company | City | geo")
    print("-" * 80)
    for user in users:

       print(
    f"{user['id']} | "
    f"{user['name']} | "
    f"{user['company']['name']} | "
    f"{user['address']['city']}"
    f"{user['address']['geo']}"
     )
    print("-" * 40)

elif response.status_code == 404:

    print("Resource not found.")

elif response.status_code == 401:

    print("Authentication required.")

elif response.status_code == 403:

    print("You don't have permission to access this resource.")

else:

    print("API request failed.")
    print(f"Status Code : {response.status_code}")

    print("API request failed.")
    print(f"Status Code : {response.status_code}")