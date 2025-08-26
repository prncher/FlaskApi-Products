from functools import wraps
import os
from flask import Flask, json, jsonify, make_response, request
import jwt
import requests


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
print(os.getpid())
port = int(os.environ.get('PORT',5000))
print('port:',port)

def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token=request.cookies.get('token')
        if not token:
            return jsonify({'error':'Authorization token is missing'}),401
        try:
            data = jwt.decode(token,app.config['SECRET_KEY'],algorithms=["HS256"])
            current_user_id = data['user_id']
        except jwt.DecodeError:
            return jsonify({'error':'Authorization token is invalid'}),401
        return f(current_user_id,*args,**kwargs)
    return decorated

with open('users.json','r') as f:
    users=json.load(f)

@app.route('/auth',methods=['POST'])
def authenticate_user():
    if request.headers['Content-Type'] != 'application/json':
        return jsonify({'error': 'Unsupported Media Type'}),415
    username = request.json.get('username')
    password = request.json.get('password')
    for user in users:
        if user['username'] == username and user['password'] == password:
            token=jwt.encode({'user_id': user['id']},app.config['SECRET_KEY'],algorithms=["HS256"])
            response = make_response(jsonify({'message':'Authentication successful'}))
            response.set_cookie('token',token)
            return response,200
    return jsonify({'error':'Invalid username or password'}),401

@app.route("/")
def index():
    return "Hello World"

@app.route("/products",methods=['GET'])
# @token_required
def get_products():
    base_url="https://services.odata.org/OData/OData.svc/Products?$format=json"
    response=requests.get(base_url)
    if response.status_code != 200:
        return jsonify({
            'error': response.json()['message']
        }),response.status_code
    #print(response.text)
    response_json = response.json()
    products=[]
    print(response_json['value'])
    for p in response_json['value']:
        products.append(p)
    return jsonify({'data':products}),200


print(__name__)
if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=port)

'''
create a virtual env namely venv
virtualenv venv

Now activate the virtual env. using =>
source venv/bin/activate

install the python packages using
pip install -r requirements.txt


docker build -t flask-server .
docker run -p 127.0.0.1:4000:5000 flask-server => first port 4000 is the containers port. 
                                                    5000 is the host machine port where the service runs.


dockrfile
========
FROM python:3.10-alpine
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
# indicates the port from the host. If the host is using 4000 from env file, change the expose.
EXPOSE 4000
CMD ["python", "./services/products.py"]
# RUN apk add bash curl --no-cache

'''