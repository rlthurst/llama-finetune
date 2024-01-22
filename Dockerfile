# Include Python
from --platform=linux/amd64 python:3.11

# Define your working directory
WORKDIR /app
COPY . .


# Install dependencies
RUN pip install -U pip setuptools
RUN pip install --extra-index-url https://download.pytorch.org/whl/test/cu118 -e .
RUN pip install -r /app/requirements.txt
