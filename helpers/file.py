def write_on_file(latest_config):
    file_path = "./last.txt"
    with open(file_path, 'w') as file:
        file.write(latest_config)
    return "OK"


def read_from_file(last_config):
    file_path = "./last.txt"
    with open(file_path, 'r') as file:
        content = file.read()
    return content

def write_on_telegram_file(telegram_config):
    file_path = "./telegram.txt"
    with open(file_path, 'w') as file:
        file.write(telegram_config)
    return "OK"

def write_on_channel_file(channel):
    file_path = "./config.txt"
    with open(file_path, 'w') as file:
        file.write(channel)
    return "OK"

def read_channel_from_file():
    file_path = "./config.txt"
    with open(file_path, 'r') as file:
        content = file.read()
    return content