import sqlite3
from datetime import datetime


class Database:
    __instance__ = None

    def __init__(self):
        if Database.__instance__ is None:
            Database.__instance__ = self
        else:
            raise Exception("You cannot create another Database class")

        self.db = sqlite3.connect("db.sqlite3")
        self.cr = self.db.cursor()
        self.cr.execute('CREATE TABLE IF NOT EXISTS `search` ( `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `search_keyword` TEXT NOT NULL, `search_date` INTEGER NOT NULL )')
        self.cr.execute('CREATE TABLE IF NOT EXISTS `search_results` ( `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `search_id` INTEGER NOT NULL, `title` TEXT, `description` TEXT, `content` TEXT, `image` TEXT, `is_saved` INTEGER, `author` TEXT, `url` TEXT)')
        self.db.commit()

    @staticmethod
    def get_instance() -> 'Database':
        """ Static method to fetch the current instance.
        """
        if not Database.__instance__:
            Database()
        return Database.__instance__

    def get_search(self, search_id: int = None) -> list:
        if search_id is not None:
            self.cr.execute('SELECT * FROM search WHERE id = ?', [search_id])
        else:
            self.cr.execute('SELECT * FROM search')
        names = [description[0] for description in self.cr.description]
        values = self.cr.fetchall()
        return self.tuple_to_dict(names=names, values=values)

    def insert_search(self, search_keyword: str) -> tuple:
        self.cr.execute('INSERT INTO search VALUES(null,?,?)', [search_keyword, datetime.now().timestamp()])
        self.db.commit()
        self.cr.execute('SELECT max(id) from search')
        return self.cr.fetchall()[0]

    def get_search_result(self, search_id: int = None) -> list:
        if search_id is not None:
            self.cr.execute('SELECT * FROM search_results WHERE search_id = ?', [search_id])
        else:
            self.cr.execute('SELECT * FROM search_results')
        names = [description[0] for description in self.cr.description]
        values = self.cr.fetchall()
        return self.tuple_to_dict(names=names, values=values)

    def inset_search_result(self, search_id: tuple, search_results: dict):
        try:
            for search_result in search_results.get('articles'):
                if not self.is_same_url_exist(search_result['url']):
                    self.cr.execute('INSERT INTO search_results VALUES(null,?, ?, ?, ?, ?, 0, ?, ?)', [search_id[0], search_result['title'], search_result['description'], search_result['content'], search_result['urlToImage'], search_result['author'], search_result['url']])
            self.db.commit()
        except Exception as e:
            print('result cannot be added', e)

    def update_search_result(self, search_result_id: int):
        self.cr.execute('UPDATE search_results SET is_saved = 1 WHERE id = ?', [search_result_id])
        self.db.commit()

    def get_saved_results(self) -> list:
        self.cr.execute('SELECT * FROM search_results WHERE is_saved = 1')
        return self.cr.fetchall()

    def is_same_url_exist(self, url: str) -> bool:
        self.cr.execute('SELECT * FROM search_results WHERE url = ?', [url])
        values = self.cr.fetchall()
        return len(values) != 0

    def tuple_to_dict(self, names: list, values: list) -> list:
        result = []
        r = {}
        for value in values:
            for i in range(len(names)):
                r[names[i]] = value[i]
            result.append(r)
            r = {}
        return result
