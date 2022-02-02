# syntax=docker/dockerfile:1

# Install Python image
FROM python:3.8-slim-buster

# Create working directory and install dependencies
WORKDIR /bitcaviar-plus

# Copy files
COPY . .

# Install package
RUN ["python", "setup.py", "install"]

# Test package
CMD ["python", "-m", "unittest", "tests.test_implementation"]