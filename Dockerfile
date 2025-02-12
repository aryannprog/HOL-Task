FROM python:3.9

# Install required packages
RUN apt-get update && apt-get install -y \
    chromium-driver \
    google-chrome-stable \
    unzip

# Set environment variables
ENV DISPLAY=:99

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app
COPY . /app
WORKDIR /app

# Run the Streamlit app
CMD ["streamlit", "run", "app.py"]
