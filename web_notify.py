from websocket import create_connection
from time import sleep
import json
import requests
from statistics import mean
from web import json2cdsData, post_to_slack


if __name__ == '__main__':
    wsslink = "wss://api.sakura.io/ws/v1/e57d2928-d318-4b1a-b291-f8ca38b8c839"
    ws = create_connection(wsslink)
    is_day = True
    threshold = 5.0
    while True:
        try:
            result = ws.recv()
            temps = json2cdsData(result)
        except KeyboardInterrupt:
            break
        print(temps)
        if isinstance(temps, list):
            temps_round = [round(elem, 1) for elem in temps]
            mean_cds = mean(temps)
            s = '{}: {}'.format(round(mean(temps), 2), temps_round)
            print(s)
            if is_day and mean_cds > threshold:
                post_to_slack('夜になりました :crescent_moon:')
                is_day = False
            elif not is_day and mean_cds < threshold:
                post_to_slack('朝になりました :sunny:')
                is_day = True
        sleep(1)
    ws.close()
