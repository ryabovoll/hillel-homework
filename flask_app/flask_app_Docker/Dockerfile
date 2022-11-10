FROM ubuntu

RUN apt-get update; apt-get install -y python3 python3-pip

WORKDIR /app
COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 5000

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python3"]
CMD ["app.py"]