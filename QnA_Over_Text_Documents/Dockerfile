#syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# FROM specifies the base image to use for the container.
FROM python:3.12.8-slim

#This will set the working directory within the container to /app
WORKDIR /app

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.

# Install the application dependencies.
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the source code into the container.
COPY ./src/Utils_AI.py .
COPY ./src/QnA_over_docs_streamlit.py .

# Expose the port that the application listens on.
EXPOSE 8501

# Run the application.
CMD ["streamlit", "run", "QnA_over_docs_streamlit.py"]
