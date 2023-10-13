import os
import requests
from dotenv import load_dotenv

if __name__ == '__main__':

    try:
        
        load_dotenv("/.env")
        
        # Get Weather Information
        responce = requests.get(
            url = "https://weather.tsukumijima.net/api/forecast",
            params = {
                "city": os.getenv("CITY"),
            }
        )
        if not responce.ok: print("Failed to get weather inf.")

        # Make a message
        cityName = (responce.json())["location"]["city"]
        result = (responce.json())["forecasts"][0]
        message = f'おはようございます！\n{result["dateLabel"]}の{cityName}の天気は {result["telop"]} 、最高気温は {result["temperature"]["max"]["celsius"]} ℃、最低気温は {result["temperature"]["min"]["celsius"]} ℃ です。'

        # Send the message to Slack
        requests.get(
            url = "http://513bot-core-send",
            params = {
                "channel": os.getenv("CHANNEL"),
                "text": message,
            }
        )
    
    except Exception as e:
        
        print(str(e))