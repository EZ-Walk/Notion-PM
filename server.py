from flask import Flask, request
from celery import Celery
import json


app = Flask(__name__)

# # Configure Celery
# app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
# app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
# celery.conf.update(app.config)

@app.route('/')
def hello_world():
    return "You've reached the Notion PM webhook server!"

# @app.route('/notion-integration', methods=['POST'])
# def notion_integration_webhook():
#     data = request.json
#     # Process the data from the Notion integration
#     print(data)
#     return 'Received Notion integration webhook'

@app.route('/repo', methods=['POST'])
def notion_integration_webhook():
    data = request.json
    # Process the data from the Notion integration

    with open('data.json', 'w') as f:
        json.dumps(data, f)
    print(data)
    return 'Received Github integration webhook'

# use another route when a release is published to github to trigger a workflow that writes the documentation to the Notion page linked at the top of the README.md
@app.route('/release', methods=['POST'])
def release_webhook():
    data = request.json
    # Process the data from the release webhook
    print(data)
    with open('release_data.json', 'w') as f:
        json.dumps(data, f)

    return 'Received release webhook'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    