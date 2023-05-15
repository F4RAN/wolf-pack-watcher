import requests

from helpers.file import write_on_channel_file

attempts = 0
while attempts < 3:
    telegram_channel = input("Please enter the Telegram channel that you want watcher focused on (default:@iSegaro): \n@ ")
    if telegram_channel:
        response = requests.get(f"https://t.me/s/{telegram_channel}")
        if response.text.find("If you have Telegram, you can contact") != -1:
            attempts += 1
            print("Channel not available. Please try again.")
            continue
        else:
            status = write_on_channel_file(telegram_channel)
            if status == "OK":
                print(f"{telegram_channel} channel is watching. :)")
                break

    else:
        telegram_channel = "iSegaro"
        status = write_on_channel_file(telegram_channel)
        print(f"{telegram_channel} channel is watching. :)")
        break

if telegram_channel is None:
    # Handle the case when the user exceeds the maximum number of attempts
    print("Invalid input. Exiting...")
    exit(2)


