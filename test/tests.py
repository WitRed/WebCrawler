from database.database import Database
from search.search import Search

if __name__ == '__main__':
    s = Search()
    db = Database.get_instance()
    keyword = 'gumus'
    results = s.search_with_keyword(keyword=keyword)
    sid = db.insert_search(search_keyword=keyword)
    db.inset_search_result(search_id=sid, search_results=results)
    db.get_saved_results()
