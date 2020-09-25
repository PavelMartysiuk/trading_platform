FROM python:3.8
ENV PYTHONUNBUFFERED 1
WORKDIR /app

COPY ./Pipfile /app/Pipfile
COPY ./Pipfile.lock /app/Pipfile.lock

RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

COPY ./entrypoint.sh /app/

RUN chmod +x entrypoint.sh

COPY . /app/

CMD ./entrypoint.sh