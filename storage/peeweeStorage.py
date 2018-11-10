from datetime import datetime

from peewee import Model, DecimalField, DateField, CharField, SqliteDatabase, MySQLDatabase, fn, TimestampField, \
    DateTimeField
from storage.base import IStorage
from os import environ, getenv

from storage.objects import BudgetItem

import logging
logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

_db_driver = getenv('DB_DRIVER', 'sqlite')
_db_name = getenv('DB_NAME', ':memory:')
_db_host = getenv('DB_HOST', None)
_db_port = int(getenv('DB_PORT', 3306))
_db_user = getenv('DB_USER', None)
_db_pass = getenv('DB_PASS', None)

_month_start_date = int(getenv('MONTH_START_DATE', 25))


# Code to initialize database driver based on ENV_VARs
if _db_driver == 'mysql':
    # Do MySql Initialization
    DB_CON = MySQLDatabase(_db_name,
                           host=_db_host,
                           port=_db_port,
                           user=_db_user,
                           password=_db_pass)
elif _db_driver == 'sqlite' or _db_driver == 'memory':
    # Do SQLite Initialization
    DB_CON = SqliteDatabase(':memory:' if _db_driver == 'memory' else _db_name)
else:
    DB_CON = None


class MBaseModel(Model):
    class Meta:
        database = DB_CON


class MBudgetItem(MBaseModel):
    Value = DecimalField(decimal_places=2)
    Date = DateTimeField(default=datetime.now)
    Description = CharField(null=True)

    @staticmethod
    def to_db(budget_item):
        """
        :param BudgetItem budget_item:
        :return MBudgetItem:
        """
        return MBudgetItem(id=budget_item.Id if budget_item.Id > 0 else None,
                           Value=budget_item.Value,
                           Date=budget_item.Date,
                           Description=budget_item.Description)

    def to_internal(self) -> BudgetItem:
        return BudgetItem(id=self.id,
                          value=self.Value,
                          date=self.Date,
                          description=self.Description)


def get_last_xth_day(day=25, now=None):
    if not now:
        now = datetime.now()
    if now.day < day:
        return datetime(now.year if now.month > 1 else (now.year - 1),
                        (now.month - 1) if now.month > 1 else 12,
                        day)
    else:
        return datetime(now.year, now.month, day)



class PeeWeeStorage(IStorage):
    def __init__(self):
        pass

    def _con(self):
        DB_CON.connect(reuse_if_open=False)
        DB_CON.create_tables([MBudgetItem])

    def _discon(self):
        if not DB_CON.is_closed():
            DB_CON.close()

    def shutdown(self):
        if not DB_CON.is_closed():
            DB_CON.close()

    def add_item(self, item):
        """
        :param BudgetItem item:
        :return:
        """
        self._con()

        i = MBudgetItem.to_db(item)
        i.save()
        DB_CON.commit()

        self._discon()

    def get_items(self):
        r = []
        f = get_last_xth_day(_month_start_date)

        self._con()
        for i in MBudgetItem.select().where(MBudgetItem.Date > f):  # type: MBudgetItem
            r.append(i.to_internal())
        self._discon()

        return r

    def delete_item(self, i):
        self._con()
        MBudgetItem.delete_by_id(i)
        DB_CON.commit()
        self._discon()

    def sum(self, items=None):
        return sum(map(lambda i: i.Value, items or self.get_items()))

    def get_string_list(self, items=None):
        return list(map(lambda i: str(i), items or self.get_items()))
