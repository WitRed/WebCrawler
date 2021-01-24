from flask import Flask
from flask_restful import Api

from view.search_result_view import SearchResultView
from view.search_view import SearchView

app = Flask(__name__)
api = Api(app)

api.add_resource(SearchView, '/api/search/<int:search_id>', '/api/search/')
api.add_resource(SearchResultView, '/api/search_result/<int:search_id>', '/api/search_result/')

if __name__ == '__main__':
    app.run()
