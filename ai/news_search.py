"""
VeriSight - News Search Module

Fetches recent articles from trusted RSS feeds.
"""

from bs4 import BeautifulSoup
import requests

RSS_FEEDS = {
    "Reuters": "https://feeds.reuters.com/reuters/topNews",
    "BBC": "http://feeds.bbci.co.uk/news/rss.xml",
    "Associated Press": "https://apnews.com/hub/ap-top-news?output=rss",
    "NPR": "https://feeds.npr.org/1001/rss.xml"
}


def fetch_feed(source, url, limit=5):
    """
    Fetch articles from one RSS feed.
    """

    articles = []

    try:
        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "VeriSight/1.0"
            }
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.content, "xml")

        items = soup.find_all("item")

        for item in items[:limit]:

            articles.append({
                "source": source,
                "title": item.title.text if item.title else "",
                "summary": item.description.text if item.description else "",
                "link": item.link.text if item.link else ""
            })

    except Exception as e:

        print(f"{source}: {e}")

    return articles


def aggregate_news(limit_per_source=5):
    """
    Collect articles from all trusted sources.
    """

    all_articles = []

    for source, url in RSS_FEEDS.items():

        all_articles.extend(
            fetch_feed(
                source,
                url,
                limit_per_source
            )
        )

    return all_articles


if __name__ == "__main__":

    news = aggregate_news()

    print(f"Retrieved {len(news)} articles\n")

    for article in news[:5]:

        print(article["source"])
        print(article["title"])
        print(article["link"])
        print("-" * 60)