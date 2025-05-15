FROM ubuntu:latest

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    xvfb \
    libxkbcommon-x11-0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-xinerama0 \
    libxcb-xfixes0 \
    qtbase5-dev \
    qt5-qmake \
    qtbase5-dev-tools \
    tomb \
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

RUN pip install --upgrade pip setuptools wheel

# Default command
CMD ["bash"]
