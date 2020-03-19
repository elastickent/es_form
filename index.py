"""Form to Elasticsearch."""


from datetime import datetime
from flask import Flask, request, render_template
from elasticsearch import Elasticsearch
es = Elasticsearch(
    ["https://ELASTICUSER:ELASTICPASSWD@ELASTICHOST:9200"],
    use_ssl=True,
    verify_certs=False
)
app = Flask(__name__, static_url_path='')


@app.route('/', methods=['GET'])
def default_form():
    """Render form."""
    return render_template('index.html')


@app.route('/post', methods=['POST'])
def post_write():
    """Write to Elasticsearch."""
    if request.method == 'POST':
        data = process_form(request)
        es.index(index='cv19', op_type='create', body=data)
        return "Request Processed.\n"


def process_form(request):
    """Add meta data to form."""
    raw_data = request.form
    data = raw_data.copy()
    data['resources'] = request.form.getlist('resources')
    if request.remote_addr == '127.0.0.1':
        data['ip'] = '100.7.27.72'
    else:
        data['ip'] = request.remote_addr
    data['user_agent'] = request.user_agent.string
    data['@timestamp'] = datetime.utcnow()
    latitude = float(data['latitude'])
    longitude = float(data['longitude'])
    data['location'] = [latitude, longitude]
    return data

app.run()
