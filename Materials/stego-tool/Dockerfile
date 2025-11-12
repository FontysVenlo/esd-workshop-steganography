FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir pillow numpy

CMD ["python", "/app/stego.py"]
