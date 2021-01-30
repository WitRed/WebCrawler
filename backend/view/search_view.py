from flask_restful import Resource
from flask import request

from backend.database.database import Database
from backend.search.search import Search


class SearchView(Resource):

    def get(self, search_id=None):
        db = Database.get_instance()
        return db.get_search(search_id=search_id)

    def put(self):
        db = Database.get_instance()
        s = Search()
        search_keyword = request.json['search_keyword']
        result = s.search_with_keyword(keyword=search_keyword)
        sid = db.insert_search(search_keyword=search_keyword)
        db.inset_search_result(search_id=sid, search_results=result)
        return sid
