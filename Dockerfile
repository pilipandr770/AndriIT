FROM python:3.10-slim

# Update and upgrade packages to fix vulnerabilities
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .

# Use a default port if PORT is not set
ENV PORT=8080

# Create entrypoint script for proper environment variable handling
COPY <<EOF /app/entrypoint.sh
#!/bin/bash
exec gunicorn --bind 0.0.0.0:${PORT} --workers 1 --threads 8 --timeout 120 run:app
EOF

RUN chmod +x /app/entrypoint.sh

# Use JSON format for CMD to properly handle signals
CMD ["./entrypoint.sh"]
