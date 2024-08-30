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
RUN apt-get install -y ffmpeg

# Expose the port that your application will run on
EXPOSE 10000

# Command to run your bot
CMD ["python3", "-m", "Bot"]
