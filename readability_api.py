from flask import Flask
from flask import request
from toolkit import WordCount
from toolkit import Readability

app = Flask(__name__)
MAX_CONTENT_LENGTH = 10000

@app.route('/')
def default():
    return homepage()

@app.route('/fkgl', methods=['POST'])
def flesch_kincaid_grade_level():

    fk = {
        'status': 'OK',
        'message': 'OK',
        'grade': '0'
    }

    if request.content_length <= MAX_CONTENT_LENGTH:
        r = Readability()
        text = str(request.get_data(as_text=True))
        grade = '{:.2f}'.format(r.flesch_kincaid_grade_level(text))
        fk['grade'] = grade
    else:
        fk['status'] = 'ERROR'
        fk['message'] = 'Too many bytes: {}. Current limit is {}.'.format(request.content_length, MAX_CONTENT_LENGTH)

    return fk

@app.route('/fres', methods=['POST'])
def flesch_reading_ease_score():

    fr = {
        'status': 'OK',
        'message': 'OK',
        'score': '0'
    }

    if request.content_length <= MAX_CONTENT_LENGTH:
        r = Readability()
        text = str(request.get_data(as_text=True))
        score = '{:.2f}'.format(r.flesch_reading_ease(text))
        fr['score'] = score
    else:
        fr['status'] = 'ERROR'
        fr['message'] = 'Too many bytes: {}. Current limit is {}.'.format(request.content_length, MAX_CONTENT_LENGTH)

    return fr

@app.route('/word-count', methods=['POST'])
def word_count():

    words = {
        'status': 'OK',
        'message': 'OK',
        'count': '0'
    }

    if request.content_length <= MAX_CONTENT_LENGTH:
        wc = WordCount()
        words['count'] = str(wc.count(request.get_data(as_text=True)))
    else:
        words['status'] = 'ERROR'
        words['message'] = 'Too many bytes: {}. Current limit is {}.'.format(request.content_length, MAX_CONTENT_LENGTH)

    return words

def homepage():

    html = """<!DOCTYPE html>
<html>
<head>
    <title>Readability API</title>
    <style>
    table, th, td {
        border: 1px solid black;
        border-collapse: collapse;
    }
    th, td {
        padding: 3px;
    }
    td {
        font-family: monospace;
    }
    </style>
</head>
<body>
    <p>This API supports the following endpoints:</p>
    <table style="border: 1px solid black">
        <thead>
        <tr>
            <th>Endpoint</th>
            <th>Method</th>
            <th>Content-Type</th>
            <th>Description</th>
        </tr>
        </thead>
        <tbody>
        <tr>
            <td>/</td>
            <td>GET</td>
            <td>N/A</td>
            <td><p>Returns this page.</p></td>
        </tr>
        <tr>
            <td>/word-count</td>
            <td>POST</td>
            <td>text/plain</td>
            <td><p>Returns the number of words in the submitted text.</p>
            <p>Body of the POST request is a string.</p>
            <p>Returns JSON. For example: <code>{count: "77", message: "OK", status: "OK"}</code></p></td>
        </tr>
        <tr>
            <td>/fkgl</td>
            <td>POST</td>
            <td>text/plain</td>
            <td><p>Returns the <b>Flesch-Kincaid Grade Level</b>.</p>
            <p>Body of the POST request is a string.</p>
            <p>Returns JSON. For example: <code>{grade: "10.77", message: "OK", status: "OK"}</code></p></td>
        </tr>
        <tr>
            <td>/fres</td>
            <td>POST</td>
            <td>text/plain</td>
            <td><p>Returns the <b>Flesch Reading Ease Score</b>.</p>
            <p>Body of the POST request is a string.</p>
            <p>Returns JSON. For example: <code>{score: "52.16", message: "OK", status: "OK"}</code></p></td>
        </tr>
        </tbody>
    </table>
    <p>If the content length is greater than 10K bytes, an error is returned that looks like this:</p>
    <pre><code>{
  "grade": "0",
  "message": "Too many bytes: 12034. Current limit is 10000.",
  "status": "ERROR"
}</code></pre>
</body>
</html>
    """

    return html


# set FLASK_APP=wsgi.py
# set FLASK_ENV=development
# see tests/tests.js for testing
