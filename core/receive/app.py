import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import requests

app = App(
    token=os.getenv("SLACK_BOT_TOKEN")
)

@app.event("app_mention")
def respond_to_mention(event, say):

    # Parse
    text = event["text"].split(None, 2)
    try:
        app_name = text[1]
        args = text[2] if len(text) == 3 else ""
    except Exception as e:
        print(e, flush=True)
        say("[core-receive] Error: Please specify application name.")
        return 0
    print([app_name, args], flush=True)

    # Send args to app
    try:
        response = requests.get(
            url=f"http://513bot-app-{app_name}",
            params={
                "channel": event["channel"],
                "args": args,
            }
        )
        if not response.ok: say(response.text)
    except Exception as e:
        print(e, flush=True)
        say(f"[core-receive] Error: Application `{app_name}` does not exist.")
        return 0

if __name__ == "__main__":

    SocketModeHandler( app, os.getenv("SLACK_APP_TOKEN") ).start()