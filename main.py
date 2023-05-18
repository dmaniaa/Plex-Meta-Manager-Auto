from flask import Flask,request, make_response
import json
import subprocess
import time

app = Flask(__name__)

logs = []

def add_log(message):
    logs.append({ 
            'date': time.strftime('%X %x %Z'),
            'message': message
        })
    
def run_pmm():
    runner = subprocess.run(["python", "plex_meta_manager.py", "-r"])
    if (runner.returncode == 0):
        add_log("PMM run finised successfully")
        response = make_response("OK", 200)
    else:
        add_log("PMM run failed")
        response = make_response("Internal Server Error", 500)
    return response

@app.route('/plex', methods=['POST'])
def plex():
    data = request.form.to_dict()
    parsed = json.loads(data['payload'])
    if (parsed['event'] == 'library.new'):
        add_log("Plex webhook received")
        response = run_pmm()
    else:
        response = make_response("No Action Taken", 200)
    return response

@app.route('/logs', methods=['GET'])
def log():
    html = 'Log: <br> <table> <tr> <th>Date</th> <th>Action</th> </tr>'
    if logs:
        for entry in logs:
            html += '<tr><td>' + entry['date'] + '</td><td>' + entry['message'] + '</td></tr>'
    html += '</table>'
    return make_response(html, 200)

@app.route('/run', methods=['GET'])
def run():
    add_log("Manual run triggered")
    return run_pmm()


if __name__ == '__main__':
    app.run(host='0.0.0.0')