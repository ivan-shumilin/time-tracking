import os


import requests
from dotenv import load_dotenv


load_dotenv()
TG_API = os.getenv('BOT_API_KEY')

whook = '0c03e761f94319.lhr.life'

r = requests.get(f'https://api.telegram.org/bot{TG_API}/setWebhook?url=https://{whook}/')

print(r.json())