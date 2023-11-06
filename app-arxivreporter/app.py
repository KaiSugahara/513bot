import polars as pl
import sqlite3
import openai
import os
from dotenv import load_dotenv
import requests
import json
import datetime

databaseName = '/log/arxiv.db'
load_dotenv("/.env")
system = """与えられた論文のアブストラクトを日本語で最大3個の箇条書き（体言止め）でまとめ，以下のフォーマットで出力してください．
```
- 要点1
- 要点2
- 要点3
```"""

def extractMetadata():

    with sqlite3.connect( databaseName ) as conn:
        df = pl.read_database("SELECT * FROM PAPERS WHERE isShown=0", conn)

    return df.sample(1).to_dicts()[0] if df.shape[0] > 0 else None

def setIsShown(id):

    with sqlite3.connect( databaseName ) as conn:
        
        c = conn.cursor()
        c.execute(f'UPDATE PAPERS SET isShown=1 WHERE id="{id}"')
        conn.commit()

def get_abstract_summary(abstract):
        
    """
        func: OpenAIのAPIを利用して，与えられたAbstractを要約
        args:
            - abstract: アブストラクト, str
        returns:
            - summary: 要約文, str
            
    """

    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Request to openai
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {'role': 'system', 'content': system},
            {'role': 'user', 'content': abstract},
        ],
        temperature=0.25,
    )
    
    # Extract content in the responce
    summary = response["choices"][0]["message"]["content"]
    
    # Convert to List
    summary = [line.replace("- ", "") for line in summary.split("\n")]
    
    return summary

if __name__ == '__main__':
    
    try:
        
        print( datetime.datetime.now().isoformat() )

        # Extract Metadata
        paperMeta = extractMetadata()

        # Check
        if paperMeta is None:
            raise Exception("Do Nothing: All papers have been already summarized.")

        # Get Summary
        summary = get_abstract_summary(paperMeta["summary"])

        # Set isShown=1
        setIsShown(paperMeta["id"])

        # Build Blocks for Slack
        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"<{paperMeta['url']}|*{paperMeta['title']}*>"
                }
            },
            {
                "type": "rich_text",
                "elements": [
                    {
                        "type": "rich_text_list",
                        "style": "bullet",
                        "elements": [
                            {
                                "type": "rich_text_section",
                                "elements": [
                                    {
                                        "type": "text",
                                        "text": line,
                                    }
                                ]
                            }
                            for line in summary
                        ]
                    }
                ]
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "plain_text",
                        "text": paperMeta["authors"] + " (" + paperMeta["updatedTime"] + " UTC)",
                    }
                ]
            },
        ]

        # Send Blocks to Slack
        requests.get(
            url = "http://513bot-core-sender",
            params = {
                "channel": os.getenv("CHANNEL"),
                "blocks": json.dumps(blocks),
            }
        )
            
    except Exception as e:
        
        print(str(e))