import os
from flask import Flask, request
from slack_sdk import WebClient

client = WebClient(
    token=os.getenv("SLACK_BOT_TOKEN")
)

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    
    # Get channel id to send a message
    channel = request.args.get('channel', '')
    if channel == "": return "Bad Request: You must specify #channel", 400
    
    # Get a message
    text = request.args.get('text', '')

    # Send the message
    result = client.chat_postMessage(
        channel = channel,
        text = text,
    )
    if result["ok"]:
        return "ok", 200
    
    return "filed to send your message.", 400
    
if __name__ == "__main__":
    
    app.run(host="0.0.0.0", port=80)