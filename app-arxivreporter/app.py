import arxiv
import datetime
import pytz
import openai
import os
import requests
from tqdm import tqdm
from dotenv import load_dotenv
import json
import time

system = """与えられた論文のアブストラクトを日本語で最大3個の箇条書き（体言止め）でまとめ，以下のフォーマットで出力してください．
```
- 要点1
- 要点2
- 要点3
```"""

def get_abstract_summary(abstract):
        
    """
        func: OpenAIのAPIを利用して，与えられたAbstractを要約
        args:
            - abstract: アブストラクト, str
        returns:
            - summary: 要約文, str
            
    """

    # Request to openai
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {'role': 'system', 'content': system},
                {'role': 'user', 'content': abstract},
            ],
            temperature=0.25,
        )
    except Exception as e:
        # Try again after 1800 sec. if openai has an error
        time.sleep(1800)
        return get_abstract_summary(abstract)
    
    # Extract content in the responce
    summary = response["choices"][0]["message"]["content"]
    
    # Convert to List
    summary = [line.replace("- ", "") for line in summary.split("\n")]
    
    return summary

if __name__ == '__main__':

    try:
        
        load_dotenv("/.env")
        
        """
            SETUP: OpenAPI
        """
        
        openai.api_key = os.getenv("OPENAI_API_KEY")
        
        """
            Extract search target date
        """
        
        date = datetime.datetime.now(pytz.timezone('Asia/Tokyo')) - datetime.timedelta(days=7) # 7日前
        date = date.strftime("%Y%m%d")
        
        """
            Search papers in arXiv
        """
        
        # Query regarding Category
        cats = ["cs.AI", "cs.IR", "cs.CV", "cs.SE", "cs.LG"]
        query_cat = "%28" + " OR ".join([f'cat:{cat}' for cat in cats]) + "%29"
        
        # Query regarding Keywords
        words = ["recommend", "recommendation", "recommender"]
        query_word = "%28" + " OR ".join([f'all:{w}' for w in words]) + "%29"
        
        # Query regarding Date
        query_date = f"submittedDate:[{date} TO {date}235959]"
        
        # Join queries
        query = " AND ".join([query_cat, query_word, query_date])
        
        # Search
        search = arxiv.Search(
            query=query,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending,
        )
        searchResults = list(arxiv.Client().results(search))
        
        """
            Formatting search results
        """
        
        results = [
            {
                "title": result.title,
                "url": result.links[0].href,
                "time": result.published.strftime("%Y/%m/%d %H:%M"),
                "authors": [author.name for author in result.authors],
                "summary": get_abstract_summary(result.summary),
            }
            for result in tqdm(searchResults)
        ]
        
        """
            Make Blocks for Slack
        """
        
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{date[:4]}/{date[4:6]}/{date[6:]}に投稿されたarXiv論文（検索対象: 推薦システム）"
                }
            },
        ]
        
        if len(results) > 0:
        
            for result in results:
                
                blocks += [
                    {
                        "type": "divider"
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*"+result["title"]+"*"
                        },
                        "accessory": {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "View"
                            },
                            "url": result["url"],
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
                                    for line in result["summary"]
                                ]
                            }
                        ]
                    },
                    {
                        "type": "context",
                        "elements": [
                            {
                                "type": "plain_text",
                                "text": ", ".join(result["authors"]) + " (" + result["time"] + " UTC)",
                            }
                        ]
                    },
                ]
                
            blocks += [
                {
                    "type": "divider"
                },
            ]
        
        else:
            
            blocks += [
                {
                    "type": "section",
                    "text": {
                        "type": "plain_text",
                        "text": "文献が見つかりませんでした :sob:",
                        "emoji": True
                    }
                }
            ]
        
        """
            Send Blocks to Slack
        """
        
        requests.get(
            url = "http://513bot-core-sender",
            params = {
                "channel": os.getenv("CHANNEL"),
                "blocks": json.dumps(blocks),
            }
        )
    
    except Exception as e:
        
        print(str(e))