import flask
import docker
import os
from flask import request, session
import random

link = flask.Flask(__name__)
link.config["DEBUG"] = True
link.secret_key="JiNO"


@link.route('/', methods=['GET'])
def home():
    return "Dusting off some old talents!!"


@link.route('/api/', methods=['GET'])
def api():
    return "Welcome to API"

provid=random.randint(500, 50000)

@link.route('/api/provisionID', methods=['GET'])
def prov():
    if 'cpu' in request.args and 'mem' in request.args:
        cp=request.args.get('cpu')
        mem=request.args.get('mem')
        print ("Input received!")
        id_no=str(provid)
        session["id_no"]=id_no
        session["cp"]=cp
        session["mem"]=mem
        return (id_no)
    else:
        return ("To provision a container CPU and MEMORY data is neccessary. You can Include this is same URL.\n For example: http://127.0.0.1:5000/api/provisionID?cpu=1&mem=300m")

@link.route('/api/container', methods=['GET'])
def jin():
    if  "id_no" in session:
        prov_id =session["id_no"]
        if request.args.get('prID')==prov_id:
            if "cp" in session:
                cpu=session["cp"]
                if "mem" in session:
                    mem=session["mem"]
                    client = docker.from_env()
                    p=client.containers.run("ubuntu:latest", stdin_open = True, tty = True, detach=True, entrypoint='/bin/bash', cpu_count=int(cpu), mem_limit=mem, privileged=True, ports={'22/tcp': ('127.0.0.1', 1331)})
                    j=str(p).split( )
                    q=j[1][:-1]
                    print (q)
                    container = client.containers.get(str(q))
                    e=vars( container )["attrs"]["NetworkSettings"]["Networks"]["bridge"]["IPAddress"]
                    print ("IP address assigned:"+e)
                    return "Docker container provisioned"
                else:
                    return "mem session went wrong"
            else:
                return "cpu not found in session"
        else:
            return "Error: comapared provision ID and is not same"
    else:
        return "Id_no part gone wrong"


link.run()
