FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code2
COPY requirements.txt /code2/
RUN pip install -r requirements.txt
COPY . /code2/
