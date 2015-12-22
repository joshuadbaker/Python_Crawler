from flask import Flask, render_template, request, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
import json
import operator
import os
from bs4 import BeautifulSoup
from IPython import embed
from rq import Queue
from rq.job import Job
from worker import conn
from urllib.parse import urlparse

import requests

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

q = Queue(connection=conn)

from models import Crawl, Image, Result, Task

def get_urls(url, max_depth, r_id):
    errors = []
 
    if max_depth == 0:
        return True
    try:
        r = requests.get(url)
    except:
        errors.append(
        "Unable to get URL. Please make sure it's valid and try again."
        )
        return {"error": errors}

    parsed_html = BeautifulSoup(r.text, 'html.parser')
    pics = parsed_html.find_all('img')
    title = parsed_html.title
    if title.string == "Not found.":
        title.string = "No Title"
    print(title.string)
    try:
        crawl = Crawl(
            name = title.string,
            url = url,
            result_id = r_id
        )

        db.session.add(crawl)
        db.session.commit()
        for pic in pics:
            if pic["src"] == None:
                pic["src"] = "No Link"
            image = Image(
                # name = pic["alt"],
                source = pic["src"],
                crawl_id = crawl.id,
                )  
            db.session.add(image)
            db.session.commit()

            # if image.name == "alt":
            #     image.name = "No Title"
            for image in crawl.images:
                print("Saving image")
                print(image.source)
                db.session.add(image)
                db.session.commit()
    except Exception as e:
        print(e)
      
      
    except:
        errors.append("Unable to add item to database.")

        return {"error": errors}
    
    links = parsed_html.find_all('a')
    base_url = url
    for link in links:
        if link.has_attr("href"):
            url = link["href"]
            if "http" in url:
                url = url
            else:
                url = base_url + link["href"]  
            if not Crawl.query.filter_by(url=url):
                print(url)
                get_urls(url, max_depth-1, r_id)
    return True             

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        
        urls = request.get_json()
        # code for array that will replace the form submission
        # urls = ['https://www.nytimes.com', 'https://www.tumblr.com']
        
        result = Result()
        db.session.add(result)
        db.session.commit()

        for url in urls:
            job = q.enqueue_call(   
                func=get_urls, args=(url, 2, result.id), result_ttl=5000
            )
            task = Task(
                completed = False,
                result_id = result.id,
                url = url,
                job_id = job.get_id()
            )
            db.session.add(task)
            db.session.commit()
 
        return jsonify(dict(id=result.id, msg=urls))
    else:   
        return render_template('index.html', results={})

@app.route("/tasks/<result_id>", methods=['GET'])
def get_tasks(result_id):
    num_completed=0 
    num_inprogress=0
    result = Result.query.filter_by(id=result_id).first()
    for task in result.tasks:
        job = Job.fetch(task.job_id, connection=conn)
        if job.result:
            num_completed += 1
        else: 
            num_in_progress += 1
    return json.dumps(dict(completed=num_completed, in_progress=num_in_progress))        
 
@app.route("/results/<result_id>", methods=['GET'])
def get_results(result_id):

    # job = Job.fetch(job_key, connection=conn)
    results = {}
    # return str(job.result), 200
    result = Result.query.filter_by(id=result_id).first()
    for crawl in result.crawls:
        image_holder = []
        results[crawl.url] = image_holder
        for image in crawl.images:
            image_holder.append(image.source) 
    return json.dumps(results)

if __name__ == '__main__':
    app.run()

