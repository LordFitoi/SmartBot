FROM python:3.7.9

WORKDIR /app

RUN pip install --upgrade pip &&\
    pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]