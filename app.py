from lib2to3.pytree import Base
from flask import Flask, render_template, request, jsonify

from datetime import datetime
import numpy as np
import pickle
# import requests
import os
from flask_cors import CORS
import random
global_containers = {'1' : 3004}
app = Flask(__name__)
CORS(app)

result = random.randint(10, 1000)
@app.route("/user/newProject", methods = ['POST'])
def create():
    dockerId = ""
    dockerIdfile = "docfile.txt"
    

    try:
        data = request.get_json(silent=True)
        print(data)
        username = data.get('username')
        projectName = data.get('projectName')
        id =  username + "_" + projectName
        # id     = "hello"
        print(id)
        if id in global_containers :
            return jsonify(
                {
                    'status' : 'userexists'
                }
            )
        global_containers[id] = list(global_containers.values())[-1] + 2
        print(global_containers)
        # print(global_containers[id])
        t = os.system(f"docker run -itdp  {global_containers[id]}-{global_containers[id] + 1}:5000-5001 githubmodified > {dockerIdfile}")
        if t == 0:
            print("Container created")
            ff = open(dockerIdfile, 'r')
            doc_id = ff.readlines()[0]
            data = {
                'status' : 'success',
                'username' : username, 
                'projectName' : projectName,
                'port' : global_containers[id],
                'id' : doc_id, 
                'liveUrl' : f"localhost/deployment/{id}/",
                'jupyter' : f"localhost:{global_containers[id] + 1}"
            }

            # create the entry in the /etc/nginx/sites-available/reverse_proxy.conf
            file1 = open('/etc/nginx/sites-available/default', 'r+')
            etc = file1.read()
            etc = etc.split('}')
            # print(etc)
            etc.pop()
            etc.pop()
            etc.append("\n\tlocation /deployment/" + f"{id}"+ "{\n\trewrite ^/deployment/" + f"{id}(.*)$ $1 break;\n\tproxy_pass http://localhost:{global_containers[id]};\n\t" + "}\n" + 
                "\n\tlocation /jupyter/" + f"{id}"+ "{\n\trewrite ^/jupyter/" + f"{id}(.*)$ $1 break;\n\tproxy_pass http://localhost:{global_containers[id] + 1};\n\t" + "}\n")
            file1.close()
            file1 = open('/etc/nginx/sites-available/default', 'w')
            for i in etc:
                file1.write(f"{i}" + "}")
            file1.close()
            # restart the nginx server
            t = os.system("sudo service nginx restart")
            # t = 0
            if(t != 0) :
                return jsonify(
                    {
                        'status' : 'failed to map the container'
                    }
                )
            return jsonify(data)
        else :
            print("failed to create container")
            data = {
                'status' : 'failed'  
            }
            return jsonify(data)
    except BaseException as e: 
        print(f"failed with exception: {e}")
        data = {
            'status' : 'failed',
        }
        return jsonify(data)
    
# @app.route("/user/createProject", methods = ['POST'])
# def create():
#     try : 
#         username = str(request.form['username'])
#         projectname = str(request.form['projectname'])
#         id = username + projectname
#         print(id)
#         if username in global_containers :
#             return "user exists"
#         global_containers[id] = global_containers[list(global_containers.values())[-1]] + 1
#         # global_containers[id] = 2
#         print(global_containers)
#         # print(global_containers[id])
#         # t = os.system(f"docker run -itdp {global_containers[id]}:5000 flaskapp")
#         # if t == 0:
#         #     print("Container created")
#         #     return "container created successfully"
#         # else :
#         #     print("failed")
#         #     return "failed to create container"
#         return "user created"
#     except: 
#         return "failed"

@app.route("/user/syncToGithub/<username>/<projectName>/<docid>", methods = ['get'])
def syncToGithub(username, projectName, docid):
    username = str(username)
    projectName = str(projectName)
    docid = str(docid)
    t = os.system(f"git checkout --orphan {username}_{projectName}")
    t = os.system(f"git checkout {username}_{projectName}")
    t = os.system(f"git add *.ipynb *.py")
    msg = "commit"
    t = os.system(f"git commit -m '{msg}'")
    t = os.system(f"git push origin {username}_{projectName}")
    data = {
        'status' : 'success',
    }
    return jsonify(data)
    
    

# @app.route("/user/<random_id>")
# def random_url(random_id):
#     if random_id not in global_containers:
#         return "URL doesn't exist"
#     r = requests.get("http://localhost:" + str(global_containers[random_id]))
#     return r.content
    
@app.route('/', methods = ['GET', 'POST'])
def home():
    # if request.method == "GET" :
    #     return render_template("index.html")
    # else :
    #     # method = request
    #     # load the model
    #     pickle_in = open("dict.pickle","rb")
    #     model = pickle.load(pickle_in)
    #     # model = load("housing/templates/housing/Dragon.joblib")
    #     CRIM = assign("CRIM")
    #     ZN = assign("ZN")
    #     INDUS = assign("INDUS")
    #     CHAS = assign("CHAS")
    #     NOX = assign("NOX")
    #     RM = assign("RM")
    #     AGE = assign("AGE")
    #     DIS = assign("DIS")
    #     RAD = assign("RAD")
    #     TAX = assign("TAX")
    #     PTRATIO = assign("PTRATIO")
    #     B = assign("B")
    #     LSTAT = assign("LSTAT")
    #     result = model.predict(np.array([[CRIM,  ZN, INDUS, CHAS, NOX,
    #    RM, AGE,  DIS, RAD , TAX,
    #    PTRATIO,  B, LSTAT]]))[0]
    #     result = result * 1000
        return render_template("index.html")


@app.route('/predict', methods = ['POST'])
def new():
    global result
    try:
        pickle_in = open("model.pickle","rb")
        model = pickle.load(pickle_in)
        # model = load("housing/templates/housing/Dragon.joblib"
        data = request.get_json(silent=True)
        total = int(data.get('arguments'))
        # result = 102.7
        result = model.predict(np.array([[float(data.get(f'{i}')) for i in range(total)]]))[0]
        # result = result * 1000
        # result = 2 / 0
        answer = {
            'result' : result
        }
        return jsonify(answer) 
    except BaseException as e:
        # print("hello")
        answer = {
            'result' : result
        }
        return answer


def assign(val) :
    ans = 0
    try :
        ans = float(request.form[val])
    
    except :
        ans = 0
    
    finally :
        return ans




if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)