FROM python:3.11-slim

RUN useradd -m appuser

WORKDIR /app

COPY requirements.txt subscriber.py /app/

RUN pip install --no-cache-dir -r requirements.txt

RUN chown -R appuser:appuser /app

USER appuser

CMD ["python", "-u", "subscriber.py"]
