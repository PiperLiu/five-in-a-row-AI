import requests

response = requests.post(
    'http://127.0.0.1:5000/aichess',
    json={'player': 1, 'last_move': 20, 'states': {30: 1, 20: 2}}
)

print(response)
