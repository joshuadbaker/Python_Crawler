# @app.route('/', methods=['GET', 'POST'])
# def index():
#   results = {}
#   if request.method == "POST":
#     url = request.for['url']
#     if 'http://' not in url[:7]:
#       url = 'http://' + url
#     job = q.enqueue_call(
#       # function for crawling url
#       func=crawl_url, args=(url,), result_ttl=5000
#     )
#     print(job.get_id())

#   return render_template('index.html', results=results)

# @app.route("/results/<job_key", methods=['GET'])
# def get_results(job_key):

#   job = Job.fetch(job_key, connection=conn)

#   if job.is_finished:
#     return str(job.result), 200
#   else:
#     return "Nay!", 202