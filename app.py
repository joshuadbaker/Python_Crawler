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
  for image in images:
    print(image["src"])

@app.route('/', methods=['GET', 'POST'])
def index():
  results = {}
  if request.method == "POST":
    url = request.form['url']
    
    job = q.enqueue_call(
      func = get_images, args=(url,), result_ttl=5000
    )

    print(job.get_id())
    # crawl = Crawl(url, count, [])
    
    # links = BeautifulSoup(r.text, 'html.parser').find_all('a')
    # for link in links:
    #   r = requests.get(link["href"])
    #   print(r.text)
  return render_template('index.html', results=results)

if __name__ == '__main__':
  app.run()