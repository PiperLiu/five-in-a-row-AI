import requests

proxies = {"http":None,"https":None}

response = requests.post(
    'https://aichess.piperliu.xyz',
    json={'player': 1, 'last_move': 20, 'states': {30: 1, 20: 2}},
    # verify=False
    proxies=proxies
)

print(response)
