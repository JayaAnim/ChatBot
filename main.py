from flask import Flask, request
import requests
import json
import subprocess

app = Flask(__name__)

bot_id = 'afb16bb3da6f031f1b318880d7'
group_id = '91430310'

@app.route("/", methods=["POST"])
def handle_request():
    with open("log.txt", "a") as file:
        file.write("received")
    if request.method == "POST":
        data = request.get_json()
        if data["name"] != "My Bot Name":
            if data["text"] == "!hello":
                message = {
                    'bot_id': bot_id,
                    'text': 'Hello!'
                }
                requests.post('https://api.groupme.com/v3/bots/post', json=message)
    return "ok"

if __name__ == "__main__":
    with open("log.txt", "a") as file:
        file.write("started")
    app.run(debug=True)