# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory in the container to /app

# Copy the current directory contents into the container at /app
COPY . .

# Install pipenv
RUN pip install pipenv

# Install any needed packages specified in Pipfile
RUN pipenv install --system --deploy

# Make port 80 available to the world outside this container
EXPOSE 8000

# Run app.py when the container launches
CMD ["python", "app.py"]
