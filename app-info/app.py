from flask import Flask, request
import requests

app = Flask(__name__)

@app.route("/", methods=["GET"])
def app_info():

    """
            指定されたチーム（複数指定可）のメンバーをシャッフルして返す
    """
    
    # Get channel id
    channel = request.args.get('channel', '')
    if channel == "": return "[app-info] Bad Request: You must specify #channel", 400
    
    # Send a message to Slack
    res = requests.get(
        url = "http://513bot-core-send",
        params = {
            "channel": channel,
            "text": channel,
        }
    )
    
    return "ok", 200

if __name__ == "__main__":
    
    app.run(host="0.0.0.0", port=80, use_reloader=True)