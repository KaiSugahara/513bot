import arxiv
import datetime
import pytz
from tqdm import tqdm
import sqlite3

databaseName = '/log/arxiv.db'

if __name__ == '__main__':
    
    try:
        
        print( datetime.datetime.now().isoformat() )
    
        """
            Extract search target date
        """

        start_date = (datetime.datetime.now(pytz.timezone('Asia/Tokyo')) - datetime.timedelta(days=90)).strftime("%Y%m%d")
        end_date = datetime.datetime.now(pytz.timezone('Asia/Tokyo')).strftime("%Y%m%d") # 今日

        """
            Search papers in arXiv
        """

        # Query regarding Category
        cats = ["cs.AI", "cs.IR", "cs.CV", "cs.SE", "cs.LG"]
        query_cat = "%28" + " OR ".join([f'cat:{cat}' for cat in cats]) + "%29"

        # Query regarding Keywords
        words = ["recommend"]
        query_word = "%28" + " OR ".join([f'all:{w}' for w in words]) + "%29"

        # Query regarding Date
        query_date = f"submittedDate:[{start_date} TO {end_date}235959]"

        # Join queries
        query = " AND ".join([query_cat, query_word, query_date])

        # Search
        search = arxiv.Search(
            query=query,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending,
            max_results=None,
        )
        results = [
            {
                "id": result.entry_id,
                "title": result.title,
                "url": result.links[0].href,
                "publishedTime": result.published.strftime("%Y/%m/%d %H:%M"),
                "updatedTime": result.updated.strftime("%Y/%m/%d %H:%M"),
                "authors": ", ".join([author.name for author in result.authors]),
                "summary": result.summary,
            }
            for result in tqdm( arxiv.Client().results(search) )
        ]
        
        """
            Save papers to database
        """

        with sqlite3.connect( databaseName ) as conn:
        
            c = conn.cursor()

            c.execute("""
                CREATE TABLE IF NOT EXISTS
                PAPERS(
                    id text primary key,
                    title text,
                    url text,
                    publishedTime text,
                    updatedTime text,
                    authors text,
                    summary text,
                    isShown integer default 0
                )
            """)

            c.executemany("""
                INSERT INTO PAPERS (id, title, url, publishedTime, updatedTime, authors, summary) VALUES (:id, :title, :url, :publishedTime, :updatedTime, :authors, :summary)
                ON CONFLICT (id)
                DO UPDATE SET id=:id, title=:title, url=:url, publishedTime=:publishedTime, updatedTime=:updatedTime, authors=:authors, summary=:summary
            """, results)

            conn.commit()
            
    except Exception as e:
        
        print(str(e))