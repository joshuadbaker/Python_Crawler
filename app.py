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

from models import Crawl, Image, Result

def get_urls(url, max_depth, r_id):
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
    if title.string == "Not found.":
        title.string = "No Title"
    # print(title.string)
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
                crawl_id = crawl.id
                )
            # if image.name == "alt":
            #     image.name = "No Title"
            for image in crawl.images:
                # print(image.source)
                db.session.add(image)
                db.session.commit()
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
                get_urls(url, max_depth-1, r_id) 

def do_your_job(url):
    result = Result()
    db.session.add(result)
    db.session.commit()
    get_urls(url, 2, result.id)
    # result.crawl = 
    # for url in urls:
    #     result.crawl = get_urls(url, 2)
    results = {}
    for crawl in result.crawls:
        # print(crawl)
        results[crawl.name] = []
        print(crawl.images)
        for image in crawl.images:
            print(image)
            # results[crawl.name].append(image.source)
    # return results
    
    # print(result.crawls)
    # return result.crawls

@app.route('/', methods=['GET', 'POST'])
def index():
    results = {}
    if request.method == "POST":
        url = request.form['url']
        # do_your_job(url)
        job = q.enqueue_call(
            func=do_your_job, args=(url,), result_ttl=5000
        )
    print(job.result, job.get_id()) 
    return render_template('index.html', results=results)

@app.route("/results/<job_key>", methods=['GET'])
def get_results(job_key):

    job = Job.fetch(job_key, connection=conn)

    if job.is_finished:
        return str(job.result), 200
        result = Result.query.filter_by(job.results)
        results = sorted(
            results
            )
        return jsonify(results)
    else:
        return "Nay!", 202

if __name__ == '__main__':
    app.run()

