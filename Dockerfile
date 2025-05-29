FROM python:3

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=1

WORKDIR /app
ADD DdjangoProject ./app
COPY requirements.txt .
RUN pip install -r requirements.txt

ENTRYPOINT ["top", "-b"]