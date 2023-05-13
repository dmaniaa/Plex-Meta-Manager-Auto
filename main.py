from flask import Flask,request, make_response
import json
import subprocess
import time

app = Flask(__name__)

logs = []

@app.route('/', methods=['POST'])
def plex():
    data = request.form.to_dict()
    parsed = json.loads(data['payload'])
    if (parsed['event'] == 'library.new'):
        logs.append({ 
            'date': time.strftime('%X %x %Z'),
            'message': 'Update webhook received'
        })
        subprocess.run(["python", "plex_meta_manager.py", "-r"])
        logs.append({ 
            'date': time.strftime('%X %x %Z'),
            'message': 'PMM run succeeded'
        })
    response = make_response("OK", 200)
    return response

@app.route('/logs', methods=['GET'])
def log():
    html = 'Log: <br> <table> <tr> <th>Date</th> <th>Action</th> </tr>'
    if logs:
        for entry in logs:
            html += '<tr><td>' + entry['date'] + '</td><td>' + entry['message'] + '</td></tr>'
    html += '</table>'
    return make_response(html, 200)


if __name__ == '__main__':
    app.run(host='0.0.0.0')