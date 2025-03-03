FROM python:3.13

WORKDIR /code

COPY ./requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

CMD ["fastapi", "run", "application/app.py", "--port", "80"]


COPY . .