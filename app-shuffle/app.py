import random
import yaml
from flask import Flask, request
import requests

app = Flask(__name__)

@app.route("/", methods=["GET"])
def app_shuffle():

    """
            指定されたチーム（複数指定可）のメンバーをシャッフルして返す
    """
    
    # Get channel id
    channel = request.args.get('channel', '')
    if channel == "": return "[app-shuffle] Bad Request: You must specify #channel", 400
    
    # Get team names
    teamNames = request.args.get('args', '')
    teamNames = teamNames.split()

    # Has at least 0 teams?
    if len(teamNames) == 0:
        return "[app-shuffle] Error: Please specify one or more teams", 400

    # Read Members
    try:
        with open("./members.yaml", "r") as f:
            members = yaml.safe_load(f.read())
    except FileNotFoundError:
        return "[app-shuffle] Error: members.yaml does not exist", 400

    # Shuffle members and save as a message
    message = []
    for team_name in teamNames:
        if team_name not in members.keys(): return "[app-shuffle] Error: You have specified a team name that does not exist in members.yml", 400
        message.append( f"{team_name}: " + "`" + "` → `".join( random.sample(members[team_name], len(members[team_name])) ) + "`")
    message = "\n".join(message)
    
    # Send a message to Slack
    res = requests.get(
        url="http://513bot-core-send",
        params={
            "channel": channel,
            "text": message,
        }
    )
    
    return "ok", 200

if __name__ == "__main__":
    
    app.run(host="0.0.0.0", port=80, use_reloader=True)