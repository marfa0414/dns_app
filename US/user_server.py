from flask import Flask,Response, request
import requests
import json
from socket import *

app = Flask(__name__)

@app.route('/')
def homepage():
    return 'test access for user service homepage'


@app.route('/fibonacci')
def readRequest():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')
    print([hostname, fs_port, number, as_ip, as_port])

    if any([hostname, fs_port, number, as_ip, as_port]) == False:
        return Response("Bad request", status=400)

    client_socket = socket(AF_INET, SOCK_DGRAM)
    message = {
        "Name": hostname,
        "Type": "A"
    }
    message = json.dumps(message)
    client_socket.sendto(message.encode(), (as_ip, int(as_port)))
    socket_response, server = client_socket.recvfrom(2048)
    socket_response = socket_response.decode()
    socket_response = json.loads(socket_response)
    url = "http://" + socket_response['Value'] + ":" + fs_port + "/fibonacci?number=" + number
    response = requests.get(url)
    print(response.text)
    return response.text,200


app.run(host='0.0.0.0',
        port=8080,
        debug=True)

