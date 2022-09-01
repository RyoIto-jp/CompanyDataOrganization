from __future__ import annotations
from typing import Any
import sqlite3


# [SQLite3 で created_at]:(https://qiita.com/kerupani129/items/0372ea29d9375e55bb36)

# dict_factoryの定義
def dict_factory(cursor: sqlite3.Cursor, row: Any) -> Any:
    d: dict[str, str | int] = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class Database:
    def __init__(self) -> None:
        self.conn: sqlite3.Connection = sqlite3.connect("database.db")
        self.conn.row_factory = dict_factory
        self.cur: sqlite3.Cursor = self.conn.cursor()

    # def __del__(self):
    #     # データベースへのコネクションを閉じる。(必須)
    #     self.conn.close()


class Users(Database):
    def __init__(self) -> None:
        super().__init__()

    def create_table_users(self):
        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT NOT NULL PRIMARY KEY,
            name TEXT NOT NULL,
            status INTEGER,
            created TEXT DEFAULT (DATETIME('now', 'localtime')) NOT NULL
        );
        ''')
        self.conn.commit()

    def insert_item(self, conn: sqlite3.Connection,
                    tablename: str = "persons"):
        cur: sqlite3.Cursor = conn.cursor()
        cur.execute(
            'INSERT INTO persons(name) values("Taro")'
        )

    def get_users(self):
        sql = '''
        SELECT id, name, status, created
        FROM users;
        '''
        self.cur.execute(sql)
        return self.cur.fetchall()

    def add_user(self, user: dict[str, str | int]) -> bool:
        sql = f'''
        INSERT INTO users
        (id, name, status, created)
        VALUES('{user["id"]}', '{user["name"]}', 1, DATETIME('now', 'localtime'));
        '''
        try:
            self.cur.execute(sql)
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        
    def del_user(self):
        sql = '''
        UPDATE users
        SET id='', name='', status=0, created=DATETIME('now', 'localtime');
        '''
        self.cur.execute(sql)

    def update_user(self):
        sql = '''
        DELETE FROM users
        WHERE id='' AND name='' AND status=0 AND created=DATETIME('now', 'localtime');
        '''
        self.cur.execute(sql)


if __name__ == '__main__':
    users = Users()
    users.create_table_users()

    result = users.add_user({
        "id": "608409",
        "name": "伊藤涼"
    })
    print("user added" if result else "Failed add user")

    print(users.get_users())
