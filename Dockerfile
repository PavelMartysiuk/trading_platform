FROM python:3.8
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY ./entrypoint.sh /app/

RUN chmod +x entrypoint.sh

COPY . /app/

CMD ./entrypoint.sh