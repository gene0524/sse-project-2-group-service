### For group service ###
FROM python:3.11

# Set the working directory in the container
WORKDIR /flask-app

# Copy the current directory contents into the container at /flask-app
COPY .. /flask-app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port available to the world outside this container
EXPOSE 3000

# Define environment variable
ENV FLASK_APP=/flask-app/api/app.py

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]