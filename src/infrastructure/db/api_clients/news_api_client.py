from newsapi import NewsApiClient


class NewsApiClientWrapper:
    def __init__(self, api_key: str):
        self.newsapi = NewsApiClient(api_key=api_key)

    def get_news(self, query: str):
        return self.newsapi.get_everything(q=query, language="en")
