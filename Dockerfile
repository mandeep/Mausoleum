FROM ubuntu:latest

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    xvfb \
    libxkbcommon-x11-0 \
    libxcb-* \
    libglib2.0 \
    freeglut3-dev \
    tomb \
    steghide \
    qrencode \
    python3.12 \
    python3.12-venv \
    python3.12-dev \
    python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.12 1 && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1

# Set working directory
WORKDIR /app

RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

RUN pip install --upgrade pip setuptools wheel

# Copy entrypoint script so that pip install is run as soon as the container starts
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh


ENTRYPOINT ["/entrypoint.sh"]
CMD ["bash"]
