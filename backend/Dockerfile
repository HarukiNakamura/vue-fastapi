FROM python:3.9.2-buster

ENV LANG C.UTF-8
ENV TZ Asia/Tokyo

COPY ./backend/requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /app

CMD ["python3.9", "/app/main.py"]