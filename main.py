from wx import App

from storage.base import GlobalStorage, ArrayStorage, Sqlite3Storage
from storage.peeweeStorage import PeeWeeStorage
from windows.NumberInputWindow import NumberInputWindow, TestWindow

if __name__ == '__main__':
    app = App(False)

    # GlobalStorage.init_storage(Sqlite3Storage('./budget.sqlite'))
    GlobalStorage.init_storage(PeeWeeStorage())

    frame = TestWindow(None)
    frame.Show(True)
    app.MainLoop()

    GlobalStorage.shutdown()
