### For api_service2 ###
FROM python:3.11

WORKDIR /flask-app

COPY /api_service2 /flask-app

RUN pip install -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=/flask-app/api/app.py

CMD ["flask", "run", "--host=0.0.0.0"]

### For client_service2 ###
# FROM python:3.11

# WORKDIR /flask-app-endpoint

# COPY /client_service2 /flask-app-endpoint

# RUN pip install -r requirements.txt

# EXPOSE 5000

# ENV FLASK_APP=/flask-app-endpoint/api/app.py
# ENV BOOK_API_URL=http://sse-book-api-server.fpf7gvfpdfacbxby.uksouth.azurecontainer.io:5000

# CMD ["flask", "run", "--host=0.0.0.0"]