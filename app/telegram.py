import time

import requests
from secrets import env_info


class Telegram:
    bot_token = env_info.telegram_bot_token
    oleg_id = 1398715343
    message_time = 0
    user_chat_ids = [oleg_id]
    text = 'Укажите код доступа Ozon (для номера +79870739395): '

    def send_message(self, t=text):
        url = f'https://api.telegram.org/bot{self.bot_token}/sendMessage'
        for chat_id in self.user_chat_ids:
            params = {'chat_id': chat_id, 'text': t}
            response = requests.post(url, data=params)
        self.message_time = int(response.json()['result']['date'])
        return response.json()

    def get_code(self):
        url = f'https://api.telegram.org/bot{self.bot_token}/getUpdates'
        for attempt in range(100):
            response = requests.get(url)
            data = response.json()
            if len(data['result']) == 0:
                time.sleep(10)
                continue
            date = int(data['result'][-1]['message']['date'])
            message = data['result'][-1]['message']['text']
            if date < self.message_time:
                time.sleep(10)
                continue
            self.send_message(t=f'Благодарю.')
            return message
        return None
