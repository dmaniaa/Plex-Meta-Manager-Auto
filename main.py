from flask import Flask,request, make_response
import json
import subprocess

app = Flask(__name__)

@app.route('/', methods=['POST'])
def plex():
    data = request.form.to_dict()
    parsed = json.loads(data['payload'])
    if (parsed['event'] == 'library.new'):
        subprocess.run(["python", "plex_meta_manager.py", "-r"])
    response = make_response("OK", 200)
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)