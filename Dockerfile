FROM python:3.10

ADD . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD [ "python3", "./bot.py" ]
