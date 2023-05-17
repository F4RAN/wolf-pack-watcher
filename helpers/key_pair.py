import requests


def get_key_pair(ip,port,cookie):
    url = f"http://{ip}:{port}/server/getNewX25519Cert"
    print("Logged-in Successfully.")
    headers = {
        'Cookie': f'session={cookie}'
    }

    response = requests.post(url, headers=headers, data={})

    return response.json()['obj']['publicKey'], response.json()['obj']['privateKey']

