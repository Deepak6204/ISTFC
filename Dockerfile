# Use a base Python image
FROM python:3.8-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libboost-all-dev \
    libatlas-base-dev \
    liblapacke-dev \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the prebuilt wheel into the Docker image
COPY dlib-19.22.0-cp38-cp38-manylinux1_x86_64.whl .

# Install the prebuilt wheel
RUN pip install dlib-19.22.0-cp38-cp38-manylinux1_x86_64.whl

# Copy requirements file and install other Python dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Define the command to run the application
CMD ["gunicorn", "myapp.wsgi:application"]
