FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . /app/

# Expose the port that Gunicorn will listen on
EXPOSE 5151

# Command to run the application using Gunicorn
CMD ["gunicorn", "--workers", "3", "--timeout", "1000", "--bind", "0.0.0.0:5151", "app:app"]