FROM python:3.11-alpine3.17

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt
RUN apk add ffmpeg

CMD ["python", "-m", "src.run"]

