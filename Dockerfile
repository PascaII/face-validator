ARG PYTHON_VERSION=3.11.6
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements-docker.txt,target=requirements-docker.txt \
    python -m pip install -r requirements-docker.txt

WORKDIR /usr/src/app

# Install necessary libraries for Dlib
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    wget \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libpng-dev \
    libopenblas-dev \
    liblapack-dev \
    && rm -rf /var/lib/apt/lists/*

# Clone Dlib repo (you can also change this to a specific version if needed)
RUN git clone https://github.com/davisking/dlib.git
WORKDIR /usr/src/app/dlib

# Build Dlib
RUN python setup.py install

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y --no-install-recommends \
      bzip2 \
      g++ \
      graphviz \
      libgl1-mesa-glx \
      libhdf5-dev \
      openmpi-bin \
      python3-tk && \
    rm -rf /var/lib/apt/lists/*

COPY . .

EXPOSE 8000

CMD cd src && uvicorn app:app --host 0.0.0.0 --port 8000
