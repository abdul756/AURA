# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the backend and frontend applications into the container
COPY . .

# Install dependencies for both applications
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y && \
    pip install --no-cache-dir -r requirements.txt

# Download the spaCy English model
RUN python -m spacy download en_core_web_sm

