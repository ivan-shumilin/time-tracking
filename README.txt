Docker команды для запуска:

docker build -t tgbotimg .

docker run --name tgbot -d --restart=always \
    -p 8000:8000 \
    -e BOT_API_KEY=6688209134:AAGEDFTzRu2rmfo2MIPdZzKEII9MktFXfYY \
    tgbotimg