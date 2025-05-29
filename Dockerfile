FROM python:3
ENV PYTHONUNBUFFERED 1
WORKDIR /app
ADD ./app
requirements.txt
RUN pip install -r requirements.txt

ENTRYPOINT ["top", "-b"]