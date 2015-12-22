import time
import json
import requests
from invoke import task

import app
    
@task             
def run_once():
    batch_id = submit().get('id')
    time.sleep(1)
    
    for i in xrange(10):        
        print(get_status(batch_id))
        time.sleep(1)
        
    print(get_results(batch_id))

@task
def test_get_urls():
    app.get_urls('http://www.tumblr.com', 3, 42)


@task
def test_get_tasks():
    print(app.get_tasks(42))

@task
def test_get_results():
    print(app.get_results(42))

@task                     
def submit():
    url = "http://localhost:5000/"
    data = json.dumps(["http://www.beatport.com/", "http://www.docker.com/"])
    headers = {'content-type': "application/json"}
    response = requests.request("POST", url, data=data, headers=headers)
    print(response.text)    
    #return response.json()

@task                 
def get_status(batch_id):
    url = "http://localhost:5000/tasks/{}".format(batch_id)
    response = requests.request("GET", url)
    print(response.text)
    #return response.json()

@task             
def get_results(batch_id):
    url = "http://localhost:5000/results/{}".format(batch_id)
    response = requests.request("GET", url)
    print(response.text)
    #return response.json()
    