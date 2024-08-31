FROM xgorn/python-phantomjs:3.9

# Copy coding files to workdir
COPY . /app/
WORKDIR /app/

ENV PYTHONUNBUFFERED=1

# Copy requirements.txt to root
COPY requirements.txt .

# Install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt
RUN apt-get update
RUN apt-get install -y ffmpeg supervisor

# Create a Supervisor configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Run supervisord to start both processes
CMD ["/usr/bin/supervisord"]
