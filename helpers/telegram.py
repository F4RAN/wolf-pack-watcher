import requests

from helpers.file import read_from_telegram_file


def send_to_telegram(link):
    bot = read_from_telegram_file()
    if bot.find('token') != -1 and bot.find('client_id') != -1:
        token = bot.split('token=')[1].split('\n')[0]
        client_id = bot.split('client_id=')[1].split('\n')[0]
        try:
            res = requests.post(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={client_id}", data={"text": link })
            print(res.text)
            if res.json()['ok']:
                return "OK"
        except:
            print("Failed to send message to telegram bot")
            return "FAILED"
    else:
        print("You don't have telegram bot for install it run 'python3 setup_telegram.py'")
        return "FAILED"
