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

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Add project files to the container
ADD . /app

# Cleanup
RUN rm -rf /app/.git
RUN rm -rf /app/.gitignore
RUN rm -rf /app/.vscode
RUN rm -rf /app/docker
RUN rm -rf /app/tests
RUN rm -f /app/log/*.log
RUN find /app -name "*.pyc" -delete

# Create a virtual environment and install dependencies
RUN rm -rf /app/venv
RUN uv venv
RUN . /app/.venv/bin/activate

# Install dependencies
RUN uv sync

# Update PATH to point to the virtual environment
ENV PATH="/app/.venv/bin:$PATH"

# Entry point to run the application
ENTRYPOINT ["uv", "run", "src/ai_mcp_net_analysis"]
