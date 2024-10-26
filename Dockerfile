FROM python:3.12
WORKDIR /app

COPY requirements.txt  main.py models.py p2p.py /app/
COPY templates /app/
RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "main.py"]
