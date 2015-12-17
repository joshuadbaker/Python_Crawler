from flask import Flask, render_template, request, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
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

from models import Crawl, Image

def get_urls(url, max_depth):
    errors = []
 
    if max_depth == 0:
        return 
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
    print(title.string)
    try:
        crawl = Crawl(
        name = title.string,
        url = url,
        # job_id = job.id
        )

        db.session.add(crawl)
        db.session.commit()
        for pic in pics:
            image = Image(
                # name = pic["alt"],
                source = pic["src"],
                crawl_id = crawl.id
                )
            # if image.name == "alt":
            #     image.name = "No Title"
            for image in crawl.images:
                print(image.source)
            db.session.add(image)
            db.session.commit()
            # return crawl.id
    except Exception as e:
        print(e)
      
      
    except:
        errors.append("Unable to add item to database.")

        return {"error": errors}
    
    links = parsed_html.find_all('a')
    # clean up logic to extract clean urls as strings not object 'Tag'
    base_url = url
    for link in links:
        if link.has_attr("href"):
            url = link["href"]
            if "http" in url:
                url = url
            else:
                url = base_url + link["href"]  
            if Crawl.query.filter_by(url=crawl.url) != url:
                get_urls(url, max_depth-1) 

def do_your_job(urls):
    result = Result(
        crawl = crawl
        )
    for url in urls:
        result.crawl = get_urls(url, 2)
        
    return result.id 

@app.route('/', methods=['GET', 'POST'])
def index():
    results = {}
    if request.method == "POST":
        url = request.form['url']
        job = q.enqueue_call(
            func=do_your_job, args=(urls,), result_ttl=5000
        )
    print(job.get_id()) 
    return render_template('index.html', results=results)

@app.route("/results/<job_key>", methods=['GET'])
def get_results(job_key):

    job = Job.fetch(job_key, connection=conn)

    if job.is_finished:
        return str(job.result), 200
        result = Result.query.filter_by(id=Result.id).first()
        results = sorted(
            result.crawl
        )
        print(results)
        return results
    else:
        return "Nay!", 202

if __name__ == '__main__':
    app.run()

