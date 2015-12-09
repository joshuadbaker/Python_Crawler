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

  try:
    
    crawl_collection = []
    crawl = Crawl(
      name=url,
      crawl_all = crawl_collection.append(crawl)
      )

    db.session.add(crawl)
    db.session.commit()

    for pic in pics:
      image = Image(
        source = pic['src'],
        crawl_id = crawl.id
        )
      db.session.add(image)
      db.session.commit()
    
  except:
    errors.append("Unable to add item to database.")
    return {"error": errors}
  
  links = parsed_html.find_all('a')
  for link in links:
    if "http" not in link["href"]:
      base_url = url
      url = base_url + link["href"]
    else:
      url = link
    if Crawl.filter_by(crawl.name) != url:
      get_urls(url, max_depth-1)



@app.route('/', methods=['GET', 'POST'])
def index():
  results = {}
  if request.method == "POST":
    
    url = request.form['url']
    get_urls(url, 2)

  #   job = q.enqueue_call(
  #     func=get_urls, args=(url, 2,), result_ttl=5000
  #   )
  # print(job.get_id()) 
  return render_template('index.html', results=results)

@app.route("/results/<job_key>", methods=['GET'])
def get_results(job_key):

  job = Job.fetch(job_key, connection=conn)

  if job.is_finished:
    crawl = Crawl.query.filter_by(id=job.result).first()
    results = sorted(
      crawl.name,
      crawl.images
      )
    print(results)
    # return jsonify(results)
if __name__ == '__main__':
  app.run()

