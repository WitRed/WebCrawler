from flask_restful import Resource
from flask import request

from database.database import Database


class SearchResultView(Resource):

    def get(self, search_id=None):
        db = Database.get_instance()
        return db.get_search_result(search_id=search_id)

    def put(self):
        db = Database.get_instance()
        search_result_id = request.json["search_result_id"]
        db.update_search_result(search_result_id=search_result_id)
