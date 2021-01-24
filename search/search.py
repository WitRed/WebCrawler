from newsapi import NewsApiClient


def get_api_key() -> str:
    with(open('api_key')) as api_key:
        return api_key.readline()


class Search:

    def __init__(self):
        self.nw = NewsApiClient(api_key=get_api_key())

    # keywords is strings
    def search_with_keyword(self, keyword) -> dict:
        return self.nw.get_everything(q=keyword, language='tr')
