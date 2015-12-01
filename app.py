from flask import Flask, render_template, request
from bs4 import BeautifulSoup
from IPython import embed
from rq import Queue
from rq.job import Job
from worker import conn
import os
import requests

app = Flask(__name__)
q = Queue(connection=conn)

# class Crawl(object):
#   name = ""
#   crawl_id = 0
#   images = []

#   def __init__(self, name, crawl_id, images):
#     self.name = name
#     self.crawl_id = crawl_id
#     self.images = images

# def make_crawl(name, crawl_id, images):
#   crawl = Crawl(name, crawl_id, images)
#   return crawl

def crawl(url, depth):
  depth += 1
  try:
    r = requests.get(url)
  except:
    errors.append(
      "Unable to get URL. Please make sure it's valid and try again."
    )
    return {"error": errors}
  
  if depth <= 2:
    print(get_images(url))
    links = BeautifulSoup(r.text, 'html.parser').find_all('a')
    for link in links:
      url = link['href']
      crawl(url, depth)
      # print(link['href'], depth)
def get_images(url):
  errors = []
  try:
    r = requests.get(url)
  except:
    errors.append(
      "Unable to get URL. Please make sure it's valid and try again."
    )
    return {"error": errors}

  images = BeautifulSoup(r.text, 'html.parser').find_all('img')
  collection = []
  for image in images:
    print(image['src'])
    # collection.append(image["src"])
    # collection


@app.route('/', methods=['GET', 'POST'])
def index():
  results = {}
  if request.method == "POST":
    url = request.form['url']
    depth = 1
    crawl(url, depth)
    # job = q.enqueue_call(
    #   func=crawl, args=(url, depth,), result_ttl=5000
    # )
    # # print(job)
    # print(job.get_id())
  return render_template('index.html', results=results)

# @app.route("/results/<job_key>", methods=['GET'])
# def get_results(job_key):
#   job = Job.fetch(job_key, connection=conn)

#   if job.is_finished:
#     result = Result.query.filter_by(id=job.result).first()
#     return str(result), 200
#   else:
#     return "Nay!", 202
if __name__ == '__main__':
  app.run()