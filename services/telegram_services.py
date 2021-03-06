import requests
from variables import *
def send_msg(text):
    print(" -TSM: sending suspecious order to captain")
    #token and chat ID are found in a private file
    url = 'https://api.telegram.org/bot' + token + '/sendMessage' + '?chat_id=' + chat_id + '&text='+ text
    result = requests.get(url)
    print(" -TSM: sending the failing order ")
    if "200" not in result:
        return 1
    print(" -TSM: Message delivery failed, restarting")
    return send_dev(text)
def send_msg_dev(text):
    print(" -TSMD: sending error message to developer")
    token = "1555294868:AAHRDgnDHkWGfTEdKrt7CbIUWXrqE6jH1_4"
    chat_id = "571211928"
    url = 'https://api.telegram.org/bot' + token + '/sendMessage' + '?chat_id=' + chat_id + '&text='+ text
    result = requests.get(url)
    print(" -TSMD: sending the follwing error ", text)
    if "200" not in result:
        return 1
    print(" -TSMD: Message delivery failed, restarting")
    return send_msg_dev(text)