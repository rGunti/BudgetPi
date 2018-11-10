from datetime import datetime
from os import getenv


CURRENCY = getenv('CURRENCY', '$')


class BudgetItem(object):
    def __init__(self,
                 id=-1,
                 value=0,
                 date=None,
                 description=""):
        self.Id = id
        self.Value = value
        self.Date = datetime.now() if not date else date
        self.Description = description

    def __str__(self) -> str:
        return "{:%d.%m.} : {} {:.2f} : {}".format(self.Date,
                                                   CURRENCY,
                                                   self.Value,
                                                   self.Description)
