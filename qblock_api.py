import flask
import docker
import os
from flask import request, session
import random
import time

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
                    p=client.containers.run("ssh_ubuntu", stdin_open = True, tty = True, detach=True, entrypoint='/bin/bash', cpu_count=int(cpu), mem_limit=mem, privileged=True, ports={'22/tcp': ('127.0.0.1', 9876)})
                    j=str(p).split( )
                    q=j[1][:-1]
                    print (q)
                    container = client.containers.get(str(q))
                    e=vars( container )["attrs"]["NetworkSettings"]["Networks"]["bridge"]["IPAddress"]
                    print ("IP address assigned:"+e)
                    os.system('sudo docker exec -it '+str(q)+' /bin/bash -c "service ssh start; apt-get install sshpass"')
                    if 'pass' not in request.args:
                        return ("no pass provided to login via ssh")
                    else:
                        os.system('sshpass -p '+str(request.args.get('pass'))+' ssh -o StrictHostKeyChecking=no '+request.args.get('USER')+'@'+e+' -C "exit"')
                        return ("successfully logged in using ssh with pass:"+request.args.get('pass')+", assigned IP "+str(e)+" port 22"+", Container ID: "+str(q))
                    return "Docker Container provisioned and tested SSH access"
                else:
                    return "mem session went wrong"
            else:
                return "cpu not found in session"
        else:
            return "Error: comapared provision ID and is not same"
    else:
        return "Id_no part gone wrong"


link.run()
