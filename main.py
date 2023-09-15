import json

import aiohttp
from fastapi import FastAPI, Request
import uvicorn


from schemas import Answer

import os
# from dotenv import load_dotenv

from geopy.distance import distance
from geopy.point import Point


def get_point(latitude: float, longitude: float) -> Point:
    return Point(latitude=latitude, longitude=longitude)

app = FastAPI()

# load_dotenv()
TG_API = os.getenv('BOT_API_KEY')

LOCATIONS = [
    {
        'name': 'Алкон',
        'location': {
            'latitude': 55.805278,
            'longitude': 37.520588,
        }
    },
    {
        'name': 'Сколково',
        'location': {
            'latitude': 55.685162,
            'longitude': 37.350982,
        }
    }
    # {
    #     'name': 'Токио сити',
    #     'location': {
    #         'latitude': 60.051600,
    #         'longitude': 30.437705,
    #     }
    # }

]


@app.post("/")
async def read_root(request: Request):
    result = await request.json()
    obj = Answer.model_validate(result)
    print(obj)

    reply_markup = {
        "keyboard":
            [
                [
                    {
                        "request_location": True,
                        "text": "Отправить локацию",
                    }
                ],
            ],
         "resize_keyboard": True,
         "one_time_keyboard": True,
    }

    # проверка, есть ли геоданные
    if obj.message.location != None:
        print('------', obj.message.reply_to_message)
        if obj.message.reply_to_message:
            target_point = get_point(obj.message.location.latitude, obj.message.location.longitude)
            dist_alkon = int(distance(
                target_point,
                get_point(LOCATIONS[0]['location']['latitude'], LOCATIONS[0]['location']['longitude'])
            ).m)
            dist_sk = int(distance(
                target_point,
                get_point(LOCATIONS[1]['location']['latitude'], LOCATIONS[1]['location']['longitude'])
            ).m)
            answer = f'Расстояние до Алкона - {dist_alkon} м\nРасстояние до Hadassah - {dist_sk} м\n'
        else:
            answer = 'Вахаха, меня так просто не хакнуть 😈'

    else:
        answer = 'Для отправки геоданных нажмите "Отправить локацию"'


    data = {
        'chat_id': obj.message.chat.id,
        'text': answer,
        'reply_markup': json.dumps(reply_markup)
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
                f'https://api.telegram.org/bot{TG_API}/sendMessage',
                data=data
        ) as response:
            print(response.status)

    return ({'status': 'OK'})


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="0.0.0.0", reload=True)


