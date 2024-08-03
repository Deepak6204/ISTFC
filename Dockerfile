# Use a base Python image
FROM python:3.8-slim

# Install system dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
    cmake \
    build-essential \
    libopencv-dev \
    python3-opencv \
    python3-pip \
    git

# Clone and build dlib from source
RUN git clone https://github.com/davisking/dlib.git && \
    chmod -R 777 dlib && \
    cd dlib && \
    mkdir build && \
    cd build && \
    cmake .. && \
    cmake --build . --config Release && \
    ldconfig && \
    make install && \
    cd .. && \
    python3 setup.py install

# Set the working directory
WORKDIR /app

# Copy requirements file and install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Define the command to run the application
CMD ["gunicorn", "myapp.wsgi:application"]
