FROM python:3.11-alpine3.17

WORKDIR /app

COPY . .

RUN apk add musl-dev gcc libffi-dev
RUN pip install -r requirements.txt
RUN apk add ffmpeg

EXPOSE 80

CMD ["python", "-m", "src.run"]

