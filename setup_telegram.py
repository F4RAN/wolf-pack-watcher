import requests

from helpers.file import write_on_telegram_file

attempts = 0
telegram_bot = None

while attempts < 3:
    telegram_bot_input = input("Do you want to use telegram bot to get new configs? (y/n): ")

    if telegram_bot_input == "y":
        telegram_bot = True
        break
    elif telegram_bot_input == "n":
        telegram_bot = False
        break
    else:
        print("Invalid input. Please enter 'y' or 'n'.")
        attempts += 1

if telegram_bot is None:
    # Handle the case when the user exceeds the maximum number of attempts
    print("Invalid input. Exiting...")
    exit(2)


attempts = 0
telegram_bot_token=None
client_id=None
while attempts < 5 and telegram_bot:
    telegram_bot_token = input("Please enter your telegram bot token: ")

    if telegram_bot_token:
        res = requests.get(f"https://api.telegram.org/bot{telegram_bot_token}/getUpdates")
        if res.json()['ok']:
            guys = res.json()['result']
            if len(guys) == 0:
                print("Please push the Start button or type /start in your bot then try again.")
                continue
            separated_guys = []
            for guy in guys:
                if {'id':guy['message']['chat']['id'], 'username':guy['message']['chat']['username']} not in separated_guys:
                    separated_guys.append({'id':guy['message']['chat']['id'], 'username':guy['message']['chat']['username']})
            string = f"Which guy you are?[1-{len(separated_guys)}]"
            for index,guy in enumerate(separated_guys):
                string += f"\n {index + 1}) @{guy['username']}"
            string += "\n:"
            selected_guy = input(string)
            if int(selected_guy) in range(1, len(separated_guys) + 1):
                client_id = selected_guy[int(selected_guy) - 1]
                content = f"token={telegram_bot_token}\nclient_id={client_id}"
                status = write_on_telegram_file(content)
                if status == "OK":
                    print("Your telegram bot registered successfully, you will get configs soon.")
                    break
                else:
                    print("Problem with telegram bot")
                    attempts += 1
                    continue
            else:
                print("Invalid Telegram Token. You can get the telegram token here: https://telegram.me/BotFather.")
                attempts += 1
                continue

        else:
            print("Invalid Telegram Token. You6084136574:AAERSKFVlT4fOyUUWTfNNN7aQ4oi_hinVi4 can get the telegram token here: https://telegram.me/BotFather.")
            attempts += 1
            continue



if telegram_bot_token is None or client_id is None:
    # Handle the case when the user exceeds the maximum number of attempts
    print("Invalid input. Exiting...")
    exit(2)
