from flask import Flask, render_template, request
import os
import requests
from IPython import embed
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
  errors = []
  results = {}
  if request.method == "POST":
    try:
      url = request.form['url']
      r = requests.get(url)
      print(r.text)
    except:
      errors.append(
        "Unable to get URL. Please make sure it's valid and try again."
      )
      return render_template('index.html', erros=errors)

  return render_template('index.html', errors=errors, results=results)

if __name__ == '__main__':
  app.run()