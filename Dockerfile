FROM ubuntu:24.04

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
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set Python 3.12 as default
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.12 1 && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1

# Set up a virtual environment and install deps inside it
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"


# Set the working directory to /app
WORKDIR /app

# Copy the entire project directory into /app in the container (ensure Docker context is correct)
COPY . /app

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip && \
    pip install PyQt5 && \
    pip install .[tests]


# Default command
CMD ["bash"]
