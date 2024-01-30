FROM python:3.11

WORKDIR /app

COPY Pipfile Pipfile.lock /app/

RUN pip install pipenv
RUN pipenv install --deploy --ignore-pipfile

COPY . /app/

CMD ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
