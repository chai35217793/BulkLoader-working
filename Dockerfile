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

# Use Gunicorn to serve the Flask app
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:$PORT"]
