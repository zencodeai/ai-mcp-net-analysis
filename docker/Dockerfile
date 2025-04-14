# Use a lightweight Linux distribution as the base image
FROM kalilinux/kali-rolling
# Set the working directory in the container
WORKDIR /app

# Install necessary dependencies and penetration testing tools
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    python3 \
    python3-pip \
    python3-venv \
    metasploit-framework \
    nmap \
    nikto \
    sqlmap \
    libcap2-bin \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Install nodejs
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
RUN apt-get install -y nodejs

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy pyproject.toml into the container
COPY pyproject.toml /app/

# Create a virtual environment and install dependencies
RUN rm -rf /app/venv
RUN uv venv
RUN . /app/.venv/bin/activate

# Install dependencies
RUN uv sync

# Update PATH to point to the virtual environment
ENV PATH="/app/venv/bin:$PATH"
