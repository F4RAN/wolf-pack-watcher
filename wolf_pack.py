import json
import re
import requests
from conf.vless import parse_vless_config, add_vless
from helpers.auth import get_credentials
from helpers.inbound_manager import check_inbounds, check_conflict_ports, handle_conflict_ports
from helpers.key_pair import get_key_pair
from helpers.file import write_on_file, read_from_file, read_channel_from_file
from helpers.xui import get_xui_credentials


def main(mode):
    localhost = "127.0.0.1"
    if mode != 'dev':
        username, password, panel_port = get_xui_credentials()
    else:
        username="admin"
        password="admin"
        panel_port = 54321

    cookie = get_credentials(ip=localhost, username=username, password=password, port=panel_port)
    if not cookie:
        print("Login Failed")
        return
    channel = read_channel_from_file()
    res = requests.get(f"https://t.me/s/{channel}")
    text = res.text
    configs = re.findall(r">.*(vless://.+<|trojan://.+<|vmess://.+<)", text)
    if len(configs) == 0:
        print("No configuration finds in channel")
        return
    latest_channel_config = configs[-1][:-1]

    if not latest_channel_config:
        print("No configuration found")
        # continue;
    last_config = read_from_file(latest_channel_config)

    if last_config == latest_channel_config:
        print("No updated configuration found")
        return

    protocol = latest_channel_config.split("://")[0]
    inbounds, inbound_parameters, biggest_id = check_inbounds(ip=localhost, port=panel_port, cookie=cookie)

    if protocol == 'vless':
        publicKey, privateKey = get_key_pair(ip=localhost, port=panel_port, cookie=cookie)
        vless_config = parse_vless_config(latest_channel_config, protocol, publicKey, privateKey)
        conflict_inbound = check_conflict_ports(port=vless_config['port'], inbounds=inbound_parameters)
        if conflict_inbound is not None:
            conflict_status = handle_conflict_ports(ip=localhost, port=panel_port, inbound=conflict_inbound, inbounds=inbounds, cookie=cookie)
            if conflict_status == "Failed":
                print("Updating port conflict problem")
                return
        status = add_vless(id=biggest_id + 1,ip=localhost, port=panel_port, config=vless_config, cookie=cookie)
        print(status)
        if status == "FAILED":
            print("Add config problem")
            return
        write_on_file(latest_channel_config)
