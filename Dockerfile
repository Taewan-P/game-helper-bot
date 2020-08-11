FROM python:3

RUN mkdir -p /usr/src/game-helper
WORKDIR /usr/src/game-helper


COPY . .
RUN pip3 install --no-cache-dir -r ./requirements.txt --default-timeout=100

ENTRYPOINT ["python3", "bot.py"]