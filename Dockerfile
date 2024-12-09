# Use the official Python slim image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current project files into the container
COPY . /app

# Install system-level dependencies
# RUN apt-get update && apt-get install -y \
#     gcc \
#     libffi-dev \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

COPY ./requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose the application port
ENTRYPOINT [ "uvicorn" ]

# Create a non-root user
# RUN useradd -m myuser
# USER myuser

# Command to run the application with Gunicorn
#CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120", "wsgi:app"]

CMD ["--host", "0.0.0.0","main:app"]