from websocket import create_connection
from time import sleep
import json
import requests
from statistics import mean


def json2cdsData(json_str: str):
    data = json.loads(json_str)
    if data['type'] == 'channels':
        temps = [elem['value'] for elem in  data['payload']['channels']]
        return temps
    else:
        return 'keepalive'


def post_to_slack(text: str):
    url = 'https://hooks.slack.com/services/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'
    headers = {'content-type': 'application/json'}
    payload = {'text': text}
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    if r.status_code != 200:
        print('Error!! status_code is not 200')


if __name__ == '__main__':
    wsslink = "wss://api.sakura.io/ws/v1/e57d2928-d318-4b1a-b291-f8ca38b8c839"
    ws = create_connection(wsslink)
    while True:
        try:
            result = ws.recv()
            temps = json2cdsData(result)
        except KeyboardInterrupt:
            break
        print(temps)
        if isinstance(temps, list):
            temps_round = [round(elem, 1) for elem in temps]
            s = '{}: {}'.format(round(mean(temps), 2), temps_round)
            post_to_slack(s)
        sleep(1)
    ws.close()
