# syntax=docker/dockerfile:1

# Install Python image
FROM python:3.8-slim-buster

# Create working directory and install dependencies
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Copy files
COPY src/bitcaviar_plus bitcaviar_plus/
COPY tests/test_app.py .

# Run script
CMD ["python3", "-u", "test_app.py"]