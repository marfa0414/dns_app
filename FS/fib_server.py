from flask import Flask, request
import json
from socket import *

app = Flask(__name__)

def get_fibonacci(n):
    if n < 2:
        return n
    fib = []
    fib.append(0)
    fib.append(1)
    for i in range(2,n+1):
        fib.append(fib[i-1]+fib[i-2])
    return fib[n]

@app.route('/')
def test():
    return 'test access home page'

@app.route('/register',methods=['POST'])
def register():
    content = request.get_json()
    hostname = content.get('hostname')
    ip = content.get('ip')
    as_ip = content.get('as_ip')
    as_port = int(content.get('as_port'))


    clientSocket = socket(AF_INET,SOCK_DGRAM)
    message = {
        "type" : "A",
        "Name" : hostname,
        "Value" : ip,
        "TTL" : 10
    }
    app_json = json.dumps(message)
    print(app_json)
    clientSocket.sendto(app_json.encode(),(as_ip,int(as_port)))
    response, serverAddress = clientSocket.recvfrom(2048)
    clientSocket.close()
    response = response.decode()
    print(response)
    return "Registration Success",201

@app.route('/fibonacci')
def fibonacci():
    print(request.args)
    num = request.args.get('number')
    if not num.isnumeric() :
        return "Bad request",400

    return str(get_fibonacci(int(num))), 200

app.run(host='0.0.0.0',
        port=9090,
        debug=True)