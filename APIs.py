import requests

# url = "http://localhost:8000/login"
base_url = "http://localhost:8000"

# response = requests.post(
#     url=url,
#     headers={
#         "X-API-Key": "secret123"
#     },
#     data={
#         "username": "Artin",
#         "password": "Artin123",
#     }
# )

# print(response.json())


def signup_fetch(username, password):
    response = requests.post(
        url=f"{base_url}/signup",
        headers={
            "X-API-Key": "secret123"
        },
        data={
            "username": username,
            "password": password,
        }
    )
    return response


def login_fetch(username, passowrd):
    response = requests.post(
        url=f"{base_url}/login",
        headers={
            "X-API-Key": "secret123"
        },
        data={
            "username": username,
            "password": passowrd,
        }
    )
    return response


def get_all_users_fetch():
    response = requests.get(
        url=f"{base_url}/get-all-users",
    )
    return response