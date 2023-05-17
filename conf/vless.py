import binascii
import json
import os
import datetime
import urllib
from urllib.parse import urlparse

import requests

from helpers.inbound_manager import get_inbound
from helpers.telegram import send_to_telegram

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
        inbound = get_inbound(id,ip, port, cookie)
        link = gen_vless_link(inbound)
        send_to_telegram(link)
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

# def send_to_telegram(id):
#
#
def gen_vless_link(inbound):
    settings = json.loads(inbound['settings'])
    stream = json.loads(vless_config['streamSettings'])
    uuid = settings['clients'][0]['id']
    port = inbound['port']
    type = stream['network']
    params = {}

    def add_param(key, value):
        if value:
            params[key] = value

    add_param("type", stream['network'])

    if type == "tcp":
        tcp = stream['tcpSettings']
        try:
            if tcp and tcp['type'] == 'http':
                request = tcp['request']
                add_param("path", ",".join(request['path']))
                index = next((i for i, header in enumerate(request['headers']) if header['name'].lower() == 'host'), -1)
                if index >= 0:
                    host = request['headers'][index]['value']
                    add_param("host", host)
                add_param("headerType", 'http')
        except KeyError as e:
            print(e)
            pass

    elif type == "kcp":
        kcp = stream['kcpSettings']
        add_param("headerType", kcp['type'])
        add_param("seed", kcp['seed'])

    elif type == "ws":
        ws = stream['wsSettings']
        add_param("path", ws['path'])
        index = next((i for i, header in enumerate(ws['headers']) if header['name'].lower() == 'host'), -1)
        if index >= 0:
            host = ws['headers'][index]['value']
            add_param("host", host)

    elif type == "http":
        http = stream['httpSettings']
        add_param("path", http['path'])
        add_param("host", http['host'])

    elif type == "quic":
        quic = stream['quicSettings']
        add_param("quicSecurity", quic['security'])
        add_param("key", quic['key'])
        add_param("headerType", quic['type'])

    elif type == "grpc":
        grpc = stream['tcpSettings']
        add_param("serviceName", grpc['serviceName'])
        if grpc['multiMode']:
            add_param("mode", "multi")

    if stream['security'] == 'tls':
        add_param("security", "tls")
        add_param("fp", stream['tls']['settings']['fingerprint'])
        add_param("alpn", stream['tls']['alpn'])
        if stream['tls']['settings']['allowInsecure']:
            add_param("allowInsecure", "1")
        if stream['tls']['server']:
            address = stream['tls']['server']
        if stream['tls']['settings']['serverName'] != '':
            add_param("sni", stream['tls']['settings']['serverName'])
        if type == "tcp" and settings['clients'][0]['flow']:
            add_param("flow", settings['clients'][0]['flow'])

    if stream['security'] == 'reality':
        add_param("security", "reality")
        add_param("pbk", stream['realitySettings']['settings']['publicKey'])
        add_param("fp", stream['realitySettings']['settings']['fingerprint'])
        if stream['realitySettings']['serverNames']:
            add_param("sni", stream['realitySettings']['serverNames'][0])
        if stream['realitySettings']['shortIds']:
            add_param("sid", stream['realitySettings']['shortIds'][0])
        if stream['realitySettings']['settings']['serverName']:
            address = stream['realitySettings']['settings']['serverName']
        if stream['realitySettings']['settings']['spiderX']:
            add_param("spx", stream['realitySettings']['settings']['spiderX'])
        if stream['network'] == 'tcp' and settings['clients'][0]['flow']:
            add_param("flow", settings['clients'][0][''])

    link = f"vless://{uuid}@{get_external_ip()}:{port}"
    url = urlparse(link)
    for key, value in params.items():
        url = url._replace(query=f"{url.query}&{key}={value}")
        url = url._replace(fragment=urllib.parse.quote(inbound['remark']))
    return url.geturl()

def get_external_ip():
    url = 'https://api.ipify.org'  # Service that returns the public IP address
    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()
        ip_address = response.text.strip()
        return ip_address
    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)}")
        return None
