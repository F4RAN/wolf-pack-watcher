import binascii
import json
import os
import datetime

import requests

vless_config = {"id": 100, "remark": "F4_TELEGRAM", "enable": True, "expiryTime": 0, "clientStats": [
    {"id": 1, "inboundId": 1, "enable": True, "email": "WOLF_PACK", "expiryTime": 0, "total": 0}], "listen": "",
                "port": 1234, "protocol": "vless",
                "settings": "{\n  \"clients\": [\n    {\n      \"email\": \"WOLF_PACK\",\n      \"enable\": true,\n      \"expiryTime\": 0,\n      \"flow\": \"xtls-rprx-vision\",\n      \"id\": \"187ecf5e-6dbf-4d63-dc42-19d40b3a36f8\",\n      \"subId\": \"\",\n      \"tgId\": \"\",\n      \"totalGB\": 0\n    }\n  ],\n  \"decryption\": \"none\",\n  \"fallbacks\": []\n}",
                "streamSettings": "{\n  \"network\": \"tcp\",\n  \"security\": \"reality\",\n  \"realitySettings\": {\n    \"show\": false,\n    \"xver\": 0,\n    \"dest\": \"www.datadoghq.com:443\",\n    \"serverNames\": [\n      \"www.datadoghq.com\"\n    ],\n    \"privateKey\": \"YFNsHL0rVHYPxCFTV9IZCuP5x7srQgXXQ0P2IBFXgWc\",\n    \"minClient\": \"\",\n    \"maxClient\": \"\",\n    \"maxTimediff\": 0,\n    \"shortIds\": [\n      \"913450117d\"\n    ],\n    \"settings\": {\n      \"publicKey\": \"2TXuaCYMGFn-_VPg1l2X1tYeuT3o5WdTNhqK7iuV9CE\",\n      \"fingerprint\": \"chrome\",\n      \"serverName\": \"\",\n      \"spiderX\": \"/\"\n    }\n  },\n  \"tcpSettings\": {\n    \"acceptProxyProtocol\": false,\n    \"header\": {\n      \"type\": \"none\"\n    }\n  }\n}",
                "tag": "inbound-443",
                "sniffing": "{\n  \"enabled\": true,\n  \"destOverride\": [\n    \"http\",\n    \"tls\",\n    \"quic\"\n  ]\n}"}


def add_vless(id,ip, port, config, cookie):
    url = f"http://{ip}:{port}/xui/API/inbounds/add"
    config['id'] = id
    payload = json.dumps(config)
    headers = {
        'Cookie': f'session={cookie}',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.json() and response.json()['success']:
        return "OK"
    else:
        print(response.text)
        return "FAILED"


def formatted_json(json_obj):
    formatted_json = json.dumps(json.loads(json.dumps(json_obj)), indent=2, ensure_ascii=False)
    formatted_json = formatted_json.replace("'", "\'")
    return formatted_json


def parse_vless_url(latest_config):
    try:
        uuid = latest_config.split("//")[1].split("@")[0]
    except IndexError:
        uuid = None
    try:
        port = latest_config.split("//")[1].split("@")[1].split(":")[1].split("?")[0]
    except IndexError:
        port = None
    try:
        trans_type = latest_config.split("type=")[1].split("&")[0]
    except IndexError:
        trans_type = None
    try:
        security = latest_config.split("security=")[1].split("&")[0]
    except IndexError:
        security = None
    try:
        fp = latest_config.split("fp=")[1].split("&")[0]
    except IndexError:
        fp = None
    try:
        sni = latest_config.split("sni=")[1].split("&")[0]
    except IndexError:
        sni = None
    try:
        flow = latest_config.split("flow=")[1].split("#")[0]
    except IndexError:
        flow = None

    return {'uuid': uuid, 'port': port, 'type': trans_type, 'security': security, 'fp': fp, 'sni': sni, 'flow': flow}


def parse_vless_config(latest_config, protocol, publicKey, privateKey):
    obj = parse_vless_url(latest_config)
    vless_config['remark'] = "WOLF-PACK-" + datetime.datetime.utcnow().strftime("%m-%d-%H:%M")
    vless_config['port'] = int(obj['port'])
    vless_config['protocol'] = protocol
    settings = json.loads(vless_config['settings'])
    streamSettings = json.loads(vless_config['streamSettings'])
    settings['clients'][0]['flow'] = obj['flow']
    settings['clients'][0]['email'] = "WOLF-PACK-" + datetime.datetime.utcnow().strftime("%m-%d-%H:%M")
    vless_config['settings'] = formatted_json(settings)
    streamSettings['security'] = obj['security']
    streamSettings['realitySettings']['settings']['fingerprint'] = obj['fp']
    streamSettings['realitySettings']['dest'] = obj['sni'] + ":443"
    streamSettings['realitySettings']['serverNames'] = [obj['sni']]
    streamSettings['shortIds'] = str(binascii.b2a_hex(os.urandom(10)))
    streamSettings['realitySettings']['privateKey'] = publicKey
    streamSettings['realitySettings']['settings']['publicKey'] = privateKey
    vless_config['streamSettings'] = formatted_json(streamSettings)
    return vless_config
