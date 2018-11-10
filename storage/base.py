import sqlite3
from datetime import datetime

from storage.objects import BudgetItem


class IStorage(object):

    def add_item(self, item):
        """
        :param object item:
        """
        raise NotImplementedError()

    def get_items(self):
        """
        :return list:
        """
        raise NotImplementedError()

    def delete_item(self, i):
        """
        :param int i:
        """
        raise NotImplementedError()

    def sum(self):
        """
        :return float:
        """
        raise NotImplementedError()

    def get_string_list(self):
        """
        :return list:
        """
        raise NotImplementedError()

    def shutdown(self):
        pass


class GlobalStorage(object):
    _INSTANCE = None

    @staticmethod
    def init_storage(storage):
        """
        :param IStorage storage:
        """
        GlobalStorage._INSTANCE = storage

    @staticmethod
    def get_storage():
        """
        :return: IStorage
        """
        return GlobalStorage._INSTANCE

    @staticmethod
    def shutdown():
        GlobalStorage._INSTANCE.shutdown()


class ArrayStorage(IStorage):
    def __init__(self):
        self._items = []

    def add_item(self, item):
        self._items.append(item)

    def get_items(self):
        return self._items

    def delete_item(self, i):
        del self._items[i]

    def sum(self):
        return sum(map(lambda i: i.Value, self._items))

    def get_string_list(self):
        return list(map(lambda i: str(i), self._items))


class Sqlite3Storage(IStorage):
    _TABLE_CREATES = [
        "CREATE TABLE IF NOT EXISTS items (" +
        "id integer PRIMARY KEY AUTOINCREMENT," +
        "value real NOT NULL," +
        "date datetime DEFAULT CURRENT_TIMESTAMP," +
        "description varchar(64)" +
        ");"
    ]

    @staticmethod
    def _create_db(con):
        """
        :param sqlite3.Connection con:
        """
        cur = con.cursor()
        for line in Sqlite3Storage._TABLE_CREATES:
            cur.execute(line)

    def __init__(self, path):
        self.con = sqlite3.connect(path)
        Sqlite3Storage._create_db(self.con)

    def add_item(self, item):
        """
        :param BudgetItem item:
        :return:
        """
        cur = self.con.cursor()
        cmd = "INSERT INTO items (value, date, description) VALUES(?, ?, ?);"
        cur.execute(cmd, (item.Value, item.Date.strftime("%Y-%m-%d %H:%M:%S"), item.Description))
        self.con.commit()

    def get_items(self):
        cur = self.con.cursor()
        cmd = "SELECT id, value, date, description FROM items;"
        cur.execute(cmd)

        rows = cur.fetchall()
        items = []

        for row in rows:
            items.append(BudgetItem(id=int(row[0]),
                                    value=float(row[1]),
                                    date=datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S"),
                                    description=row[3]))

        return items

    def delete_item(self, i):
        cur = self.con.cursor()
        cmd = "DELETE FROM items WHERE id = ?;"

        cur.execute(cmd, (i,))
        self.con.commit()

    def sum(self):
        cur = self.con.cursor()
        cmd = "SELECT SUM(value) FROM items;"

        cur.execute(cmd)
        return float(cur.fetchone()[0] or '0')

    def get_string_list(self, input=None):
        return list(map(lambda i: str(i), input or self.get_items()))

    def shutdown(self):
        self.con.close()
