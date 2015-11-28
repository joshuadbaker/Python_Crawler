from flask import Flask, render_template, request
from bs4 import BeautifulSoup
from IPython import embed
import os
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
  errors = []
  results = {}
  if request.method == "POST":
    try:
      url = request.form['url']
      r = requests.get(url)
      # print(r.text)
    except:
      errors.append(
        "Unable to get URL. Please make sure it's valid and try again."
      )
      return render_template('index.html', errors=errors)
  if r:
    images = BeautifulSoup(r.text, 'html.parser').find_all('img')
    for image in images:
      print(image["src"])
      # print(image)  
  return render_template('index.html', errors=errors, results=results)

if __name__ == '__main__':
  app.run()