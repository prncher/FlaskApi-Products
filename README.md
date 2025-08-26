# FlaskApi-Products
This is a server in python using Flask and run on docker container. It shows products fetched using OData.

# Steps to run the api.
1. pip install virtualenv
2. virtualenv venv
3. source ./venv/bin/activate
4. pip install -r ./requirements.txt
5. docker build -t flask-server .
6. docker run -p 127.0.0.1:4000:5000 flask-server
