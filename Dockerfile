# Use official Python image
FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    chromium-driver \
    google-chrome-stable \
    fonts-liberation \
    libappindicator3-1 \
    libnspr4 \
    libnss3 \
    xdg-utils

# Install dependencies
RUN apt-get update && apt-get install -y \
    chromium chromium-driver

# Set environment variables for Selenium
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_BIN=/usr/bin/chromedriver

# Install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app
WORKDIR /app

# Set up Streamlit to run
CMD ["streamlit", "run", "app.py"]
