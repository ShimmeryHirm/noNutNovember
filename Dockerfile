FROM python:3.7-slim

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY main.py /bin
COPY config.py /bin

COPY core /bin

ENTRYPOINT ["python3" "/bin/main.py"]
