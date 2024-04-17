# Use the official Python image
FROM python:3.10-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV FLASK_APP=main.py

# Optional: Set environment variables for character encoding (if needed)
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Run app.py when the container launches
CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0"]

