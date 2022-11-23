FROM python:alpine

WORKDIR /API-tic-tac

COPY ./requirements.txt .

RUN pip install -r ./requirements.txt

COPY . .

CMD [ "python", "API/main.py"]
