import os
import requests
from dotenv import load_dotenv
import re
import datetime

if __name__ == '__main__':

    try:
        
        load_dotenv("/.env")
        
        # Get Current Time
        currentTime = datetime.datetime.now()
        week_map = {0: "月", 1: "火", 2: "水", 3: "木", 4: "金", 5: "土", 6: "日",}
        
        # Get Weather Information
        responce = requests.get(
            url = "https://weather.tsukumijima.net/api/forecast",
            params = {
                "city": os.getenv("CITY"),
            }
        )
        if not responce.ok: print("Failed to get weather inf.")
        
        # Extract Required Inf.
        forecast = responce.json()
        cityName = forecast["location"]["city"]
        day = forecast["forecasts"][0]["dateLabel"]
        telop = forecast["forecasts"][0]["telop"]
        minTemp = val if (val := forecast["forecasts"][0]["temperature"]["min"]["celsius"]) is not None else "-"
        maxTemp = val if (val := forecast["forecasts"][0]["temperature"]["max"]["celsius"]) is not None else "-"
        description = forecast["description"]["text"]

        # Format the Description
        description = re.sub("\n\n【関東甲信地方】(.*)", "", description, flags=(re.MULTILINE | re.DOTALL))
        description = "> " + description.replace("\n\n", "\n").replace("\u3000", "").replace("\n", "\n> ")

        # Make a message
        message = f'おはようございます。{week_map.get(currentTime.weekday())}曜日です！\n{cityName}の天気は {telop} 、最高気温は {maxTemp} ℃、最低気温は {minTemp} ℃ の予報です。\n{description}'

        # Send the message to Slack
        requests.get(
            url = "http://513bot-core-sender",
            params = {
                "channel": os.getenv("CHANNEL"),
                "text": message,
            }
        )
    
    except Exception as e:
        
        print(str(e))