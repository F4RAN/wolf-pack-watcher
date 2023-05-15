import subprocess

def get_xui_credentials():
    command = 'x-ui'
    input_data = '7\n'

    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               universal_newlines=True)
    output, _ = process.communicate(input_data)

    # Print the captured output
    log = output.split("[INF]")[1]
    username = log.split("username: ")[1].split("\n")[0]
    password = log.split("userpasswd: ")[1].split("\n")[0]
    port = log.split("port: ")[1]

    return username, password, port