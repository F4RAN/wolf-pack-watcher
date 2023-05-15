import json
import random

import requests


def check_inbounds(ip, port, cookie):
    url = f"http://{ip}:{port}/xui/API/inbounds/"
    headers = {
        'Cookie': f'session={cookie}'
    }
    response = requests.get(url, headers=headers)
    if response.json() and response.json()['success']:
        result = []
        inbounds = response.json()['obj']
        maxId = 0
        for inbound in inbounds:
            if int(inbound['id']) > maxId:
                maxId = int(inbound['id'])
            result.append(inbound)
        return inbounds, result, maxId
    else:
        print(response.text)
        return "Failed"


def handle_conflict_ports(ip, port, inbound, inbounds, cookie):
    find_new_port = False
    while not find_new_port:
        new_port = random.randint(10000, 65535)
        for inbound in inbounds:
            if inbound['port'] == new_port:
                continue
        find_new_port = True
    inbound['port'] = new_port
    headers = {
        'Cookie': f'session={cookie}',
        'Content-Type': 'application/json'
    }
    response = requests.post(f'http://{ip}:{port}/xui/API/inbounds/update/{str(inbound["id"])}', headers=headers, data=json.dumps(inbound))

    if response.json() and response.json()['success']:
        return "OK"
    else:
        print(response.text)
        return "Failed"


def check_conflict_ports(port, inbounds):

    for inbound in inbounds:
        if inbound['port'] == port:
            print(inbound['port'],port)
            return inbound
