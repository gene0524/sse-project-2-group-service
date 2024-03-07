### For group service ###
FROM python:3.11

# Set the working directory in the container
WORKDIR /flask-app

# Copy the current directory contents into the container at /flask-app
COPY /sse-team-project-2-group-service /flask-app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run app.py when the container launches
CMD ["flask", "run"]