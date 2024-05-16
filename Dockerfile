# Use the official Python 3.11 slim image as a parent image
FROM python:3.11.4-slim-bullseye

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
# PYTHONDONTWRITEBYTECODE 1: This tells Python to not write .pyc files which are the compiled bytecode files. This is useful in a development environment because it prevents the creation of these files in your container, which can help avoid issues with volume mounting where the host and the container might have different Python bytecode.

ENV PYTHONFAULTHANDLER 1
# PYTHONFAULTHANDLER 1: This enables the fault handler feature, which can be useful for debugging. When a fatal error occurs (like a segmentation fault), the fault handler will output a traceback for all Python threads, which can help diagnose the issue.

ENV PYTHONUNBUFFERED 1
# PYTHONUNBUFFERED 1: This sets the stdout and stderr streams to be unbuffered. This can be particularly useful in a Docker container, as it ensures that you see the output of your application (like print statements) in real-time without being held in a buffer. This can help with logging and debugging in real-time.

# Set work directory
WORKDIR /src/app/

# Install system dependencies
RUN apt-get update && \
apt-get install -y \
build-essential \
gcc \
python3-dev \
libffi-dev \
libpng-dev \
libjpeg-dev \
openjdk-11-jdk \
nano \
dos2unix \
wget && \
apt-get clean

# Set JAVA_HOME environment variable
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/
RUN export JAVA_HOME

# Download Apache Tika server JAR and its MD5 checksum
RUN wget -O /src/app/tika-server.jar http://search.maven.org/remotecontent?filepath=org/apache/tika/tika-server-standard/2.6.0/tika-server-standard-2.6.0.jar && \
    wget -O /src/app/tika-server.jar.md5 http://search.maven.org/remotecontent?filepath=org/apache/tika/tika-server-standard/2.6.0/tika-server-standard-2.6.0.jar.md5 && \
    cp /src/app/tika-server.jar /tmp/tika-server.jar && \
    cp /src/app/tika-server.jar.md5 /tmp/tika-server.jar.md5

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /src/app/
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /src/app/
COPY . /src/app/