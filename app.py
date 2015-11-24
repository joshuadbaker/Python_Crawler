from rq import Queue
from rq.job import Job
from worker import conn

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
# db = SQLAlchemy(app)

a = Queue(connection=conn)

from models import * 