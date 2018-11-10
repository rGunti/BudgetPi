from wx import Button, EVT_BUTTON, StaticText, Font, FONTFAMILY_DEFAULT, FONTSTYLE_NORMAL, FONTWEIGHT_NORMAL, ListBox, \
    NOT_FOUND, Dialog, BORDER_NONE, BoxSizer, ID_OK

from piwindows.base import BaseWindow, BaseWindowPanel
from piwindows.const import Colour, get_colour
from storage.base import GlobalStorage


class EntryListDialog(Dialog):
    def __init__(self, parent):
        Dialog.__init__(self,
                        parent,
                        title=u"Entries",
                        size=(320, 240),
                        style=BORDER_NONE)

        pnl = EntryListWindowPanel(self)
        self._pnl = pnl

        self._sizer = BoxSizer()
        self._sizer.Clear()
        self._sizer.Add(self._pnl)
        self.SetSizer(self._sizer)


class EntryListWindowPanel(BaseWindowPanel):
    def __init__(self, parent):
        BaseWindowPanel.__init__(self,
                                 parent,
                                 bg_color=Colour.BLACK,
                                 fg_color=Colour.WHITE)

        self._title_label = StaticText(self,
                                       pos=(110, 10),
                                       size=(100, 30),
                                       label=u"Entries")
        self._title_label.SetFont(Font(20, FONTFAMILY_DEFAULT, FONTSTYLE_NORMAL, FONTWEIGHT_NORMAL))

        self._back_button = Button(self,
                                   -1,
                                   "< Back",
                                   pos=(10, 10),
                                   size=(70, 30))
        self._back_button.SetBackgroundColour(get_colour(0x333333))
        self._back_button.SetForegroundColour(Colour.WHITE)

        self._delete_button = Button(self,
                                     -1,
                                     "Del",
                                     pos=(240, 10),
                                     size=(70, 30))
        self._delete_button.SetBackgroundColour(Colour.RED)
        self._delete_button.SetForegroundColour(Colour.WHITE)

        self._list_control = ListBox(self,
                                     pos=(10, 50),
                                     size=(295, 170))
        self._list_control.SetBackgroundColour(Colour.BLACK)
        self._list_control.SetForegroundColour(Colour.WHITE)

        self._items = GlobalStorage.get_storage().get_items()
        self._list_control.SetItems(GlobalStorage.get_storage().get_string_list(self._items))

        self.Bind(EVT_BUTTON, self._back_button_click, self._back_button)
        self.Bind(EVT_BUTTON, self._delete_button_click, self._delete_button)

    def _back_button_click(self, e):
        self.GetParent().EndModal(ID_OK)

    def _delete_button_click(self, e):
        sel = self._list_control.GetSelection()
        if sel == NOT_FOUND:
            return
        else:
            item = self._items[sel]
            GlobalStorage.get_storage().delete_item(item.Id)

            self._items = GlobalStorage.get_storage().get_items()
            self._list_control.SetItems(GlobalStorage.get_storage().get_string_list(self._items))
