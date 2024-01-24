# Include Python
from --platform=linux/amd64 python:3.11

# Define your working directory
WORKDIR /app

# Virtual environment
ENV VENV /opt/venv
RUN python3 -m venv ${VENV}
ENV PATH="${VENV}/bin:$PATH"

COPY requirements.txt .
COPY pyproject.toml .

# Install dependencies
RUN pip install -U pip setuptools
RUN pip install --extra-index-url https://download.pytorch.org/whl/test/cu118 -e .
RUN pip install -r /app/requirements.txt

COPY . .