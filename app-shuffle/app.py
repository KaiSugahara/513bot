import random
import yaml
from flask import Flask, request
import requests
import json

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
    teamNames = [name.upper() for name in teamNames] # Convert team name to uppercase

    # Has at least 0 teams?
    if len(teamNames) == 0:
        return "[app-shuffle] Error: Please specify one or more teams", 400

    # Read Members
    try:
        with open("./members.yaml", "r") as f:
            members = yaml.safe_load(f.read())
            members = {key.upper(): val for key, val in members.items()} # Convert team name to uppercase
    except FileNotFoundError:
        return "[app-shuffle] Error: members.yaml does not exist", 400

    # Shuffle members and save as Block
    blocks = []
    for team_name in teamNames:
        # Check whether the team name exist
        if team_name not in members.keys():
            return "[app-shuffle] Error: You have specified a team name that does not exist in members.yml", 400
        # Add block
        blocks += [
            {
                "type": "context",
                "elements": [
                    {
                        "type": "plain_text",
                        "text": f"Group {team_name}:",
                    }
                ]
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": "`" + "` → `".join( random.sample(members[team_name], len(members[team_name])) ) + "`",
                    }
                ]
            },
        ]
    
    # Send Blocks to Slack
    requests.get(
        url="http://513bot-core-sender",
        params={
            "channel": channel,
            "blocks": json.dumps(blocks),
        }
    )
    
    return "ok", 200

if __name__ == "__main__":
    
    app.run(host="0.0.0.0", port=80, use_reloader=True)