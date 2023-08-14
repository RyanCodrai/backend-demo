FROM python:3.9.13-slim
WORKDIR /usr/src/app

# Ensure operating system is uing the most up to date packages
RUN apt-get update

# Install python packages
COPY requirements.txt ./
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Copy application files into environment
COPY . .

WORKDIR /usr/src/app/src

# Create logs folder if it doesn't already exist
RUN mkdir -p logs

# Launch api on port 8080
EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]