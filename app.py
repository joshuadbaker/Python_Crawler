from flask import Flask, render_template, request
from flask import jsonify
from bs4 import BeautifulSoup
from IPython import embed
from rq import Queue
from rq.job import Job
from worker import conn
from urllib.parse import urlparse
import os
import requests

app = Flask(__name__)
q = Queue(connection=conn)

class Crawl(object):
  name = ""
  crawl_id = 0
  images = []

  def __init__(self, name, crawl_id, images):
    self.name = name
    self.crawl_id = crawl_id
    self.images = images

  def serialize(self):
    return {
      'name': self.name,
      'crawl_id': self.crawl_id,
      'images': self.images
    }

def create_crawl():
  return crawl

def get_urls(url, max_depth):
  base_url = url 
  if max_depth == 0:
    return
  # try:
  r = requests.get(url)
  # except:
  #   errors.append(
  #     "Unable to get URL. Please make sure it's valid and try again."
  #   )
  #   return {"error": errors}
  
  links = BeautifulSoup(r.text, 'html.parser').find_all('a')
  urls = []
  for link in links:
    url = base_url + link["href"]
    get_images(url)
    urls.append(url)
    
    # return urls
    # urls = []
    # urls.append(link['href'])
    # # link['href']
    # # get_images(url)
    # print(urls)
    get_urls(url, max_depth-1)

    
  
def get_images(url):
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
    # print((image['src'])
    collection.append(image["src"])
    print(collection)
  return collection

@app.route('/', methods=['GET', 'POST'])
def index():
  results = {}
  if request.method == "POST":
    url = request.form['url']
    # get_urls(url, 1)
    job = q.enqueue_call(
      func=get_urls, args=(url, 1), result_ttl=5000
    )
    print(job.get_id)
    # create_crawl()
    # crawl.name = url
    # crawl.images = get_images(url)
    # crawl.crawl_id = job.get_id()
    # # results = jsonify(crawl_name=(crawl.name), crawl_id=(crawl.crawl_id), crawl_images=(crawl.images))
    # print(crawl.crawl_id)
  return render_template('index.html', results=results)

@app.route("/results/<job_key>", methods=['GET'])
def get_results(job_key):
  job = Job.fetch(job_key, connection=conn)
  results = jsonify(crawl_name=(crawl.name), crawl_id=(crawl.crawl_id), crawl_images=(crawl.images))
  return results
if __name__ == '__main__':
  app.run()