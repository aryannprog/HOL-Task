# Use Python base image
FROM python:3.9-slim

# Install necessary system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    ca-certificates \
    fonts-liberation \
    libappindicator3-1 \
    libnspr4 \
    libnss3 \
    xdg-utils 

# Add Google Chrome repository securely
RUN mkdir -p /etc/apt/keyrings && \
    wget -q -O /etc/apt/keyrings/google-chrome-keyring.gpg https://dl.google.com/linux/linux_signing_key.pub && \
    echo "deb [signed-by=/etc/apt/keyrings/google-chrome-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google-chrome.list > /dev/null

# Install Google Chrome & ChromeDriver
RUN apt-get update && apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Install ChromeDriver manually
RUN wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm /tmp/chromedriver.zip

# Set environment variable for ChromeDriver
ENV PATH="/usr/local/bin:${PATH}"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Command to run your application
CMD ["python", "app.py"]
