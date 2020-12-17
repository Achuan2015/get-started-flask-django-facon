from flask import Flask
from flask import request
from flask_json import FlaskJSON, JsonError, as_json
import jieba
app = Flask(__name__)
json = FlaskJSON(app)

token = lambda x:list(jieba.cut(x))

@app.route('/api/token', methods=['POST'])
@as_json
def test():
    data = request.get_json(force=False, silent=False, cache=True)
    try:
        response = token(data['text'])
    except (KeyError, TypeError, ValueError):
        raise JsonError(description='Invalid value.')
    return response
