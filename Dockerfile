FROM xgorn/python-phantomjs:3.9

# Copy coding files to workdir
COPY . /app/
WORKDIR /app/

ENV PYTHONUNBUFFERED=1

# Copy requirements.txt to root
COPY requirements.txt .

# Install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y ffmpeg

# Make the script executable
RUN chmod +x start.sh

# Run the startup script
CMD ["./start.sh"]
