# Use an official Python runtime as a parent image
FROM python:3.11.3

RUN apt-get install fluidsynth
# Set the working directory in the container to /app

# Copy the current directory contents into the container at /app
COPY ./websockets/python/* .

RUN pip install aiohttp
RUN pip install python-socketio
RUN pip install supabase
RUN pip install requests
RUN pip install requests_toolbelt
RUN pip install flask
RUN pip install eventlet
RUN pip install flask-socketio
# Install pipenv
# RUN pip install pipenv
#cod rares

RUN pip install midi2audio
RUN pip install MIDIUtil
RUN pip install numpy
RUN pip install opencv-python

# Install any needed packages specified in Pipfile
# RUN pipenv install --system --deploy

# Make port 80 available to the world outside this container
EXPOSE 8000

# Run app.py when the container launches
CMD ["python", "flasksocket.py"]
