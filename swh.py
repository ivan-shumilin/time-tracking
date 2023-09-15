import os
import requests


TG_API = os.getenv('BOT_API_KEY')

whook = 'hr.petrushkagroup.ru'

r = requests.get(f'https://api.telegram.org/bot{TG_API}/setWebhook?url=https://{whook}/')

print(r.json())