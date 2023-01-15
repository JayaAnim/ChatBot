from flask import Flask, request
import requests
import json
import subprocess

app = Flask(__name__)

bot_map = {'91430310': 'afb16bb3da6f031f1b318880d7', '90985439': 'df69f0cfd71fff962bd9b3d6bf'}

@app.route("/", methods=["POST"])
def handle_request():
    if request.method == "POST":
        data = request.get_json()
        print(data)
        #Ensure no self reply
        if data["sender_type"] == "user":
            send_message(data['text'], data['group_id'])

    return "ok"

def send_message(msg, group_id):
    print(group_id)
    print(bot_map[group_id])
    message = {
        'bot_id': bot_map[group_id],
        'text': msg
    }
    requests.post('https://api.groupme.com/v3/bots/post', json=message)
    return

if __name__ == "__main__":
    app.run(debug=True)