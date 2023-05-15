from urllib.parse import quote

import requests


def get_credentials(ip, username, password, port):
    login_endpoint = f'http://{ip}:{port}/login?username={quote(username)}&password={quote(password)}'
    print(login_endpoint)
    res = requests.post(login_endpoint)
    cookie = res.cookies.values()[0]
    return cookie