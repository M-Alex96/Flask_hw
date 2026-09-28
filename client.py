import requests

response = requests.post(
    "http://127.0.0.1:5000/users",
    json = {"name": "user_1", "password": "1234"},
    )

response = requests.get(
    "http://127.0.0.1:5000/users/1",
)

response = requests.patch(
    "http://127.0.0.1:5000/users/1",
    json = {"name": "new_name", "password": "1234"},
)

# response = requests.delete(
#     "http://127.0.0.1:5000/users/1",
# )

response = requests.post(
    "http://127.0.0.1:5000/advertisements",
    json = {"title": "Ищу работу", "description": "ИИ забрал мою работу, ищу новую", "owner_id": 1})

response = requests.get(
    "http://127.0.0.1:5000/advertisements/1",
)

response = requests.patch(
    "http://127.0.0.1:5000/advertisements/1",
    json = {"title": "Всё ещё ищу работу", "description": "1234 отклика и всё без результата"},
)

response = requests.delete(
    "http://127.0.0.1:5000/advertisements/1",
)

print(response.status_code)
print(response.json())