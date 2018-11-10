from datetime import datetime
from time import sleep

from wx import Button, EVT_BUTTON, Dialog, BoxSizer, ID_OK, ID_CANCEL, BORDER_NONE, FontInfo, Font, FONTFAMILY_DEFAULT, \
    FONTSTYLE_NORMAL, FONTWEIGHT_NORMAL, EVT_TIMER, Timer, StaticText, ListBox
from wx.core import CommandEvent
from wx.lib.gizmos import LEDNumberCtrl, LED_ALIGN_RIGHT

from piwindows.base import BaseWindow, BaseWindowPanel
from piwindows.const import Colour, get_colour
from storage.base import GlobalStorage
from storage.objects import BudgetItem
from windows.Listings import EntryListDialog


class TestWindow(BaseWindow):
    CATEGORIES = [
        'Groceries & Supplies',
        'Eating Out',
        'Fuel',
        'Car Repair & Maint.',
        'Other'
    ]

    def __init__(self, parent):
        BaseWindow.__init__(self,
                            parent,
                            title="Number Input",
                            size=(320, 240))

        pnl = TestPanel(self)
        self._set_panel(pnl)
        self._pnl = pnl

        self.Bind(EVT_BUTTON, self.on_open, pnl.open_button)
        self.Bind(EVT_BUTTON, self.on_close, pnl.close_button)
        self.Bind(EVT_BUTTON, self.on_list, pnl.list_button)

    def on_open(self, e):
        num = NumberInputWindow(self)
        cat = CategoryInputWindow(self, categories=TestWindow.CATEGORIES)

        if num.ShowModal() != ID_OK:
            return

        if cat.ShowModal() != ID_OK:
            return

        o = BudgetItem(value=num.get_value(),
                       description=cat.get_value())
        GlobalStorage.get_storage().add_item(o)

        self._pnl.set_display(GlobalStorage.get_storage().sum())

    def on_close(self, e):
        self.Close()

    def on_list(self, e):
        w = EntryListDialog(self)
        w.ShowModal()

        self._pnl.set_display(GlobalStorage.get_storage().sum())

    def Show(self, show=True):
        super().Show(show)
        self._pnl.set_display(GlobalStorage.get_storage().sum())


class TestPanel(BaseWindowPanel):
    def __init__(self, parent):
        BaseWindowPanel.__init__(self,
                                 parent,
                                 bg_color=Colour.BLACK,
                                 fg_color=Colour.WHITE)

        self._caption_label = StaticText(self,
                                         pos=(70, 5),
                                         size=(20, 0),
                                         label=u"This month, we spent")
        self._caption_label.SetFont(Font(13, FONTFAMILY_DEFAULT, FONTSTYLE_NORMAL, FONTWEIGHT_NORMAL))

        self._display = LEDNumberCtrl(self,
                                      pos=(0, 30),
                                      size=(320, 90),
                                      style=LED_ALIGN_RIGHT)
        self._display.SetValue("0.00")

        self._date_display = LEDNumberCtrl(self,
                                           pos=(110, 150),
                                           size=(210, 40),
                                           style=LED_ALIGN_RIGHT)
        self._date_display.SetValue("--.--.--")

        self._clock_display = LEDNumberCtrl(self,
                                            pos=(110, 190),
                                            size=(210, 50),
                                            style=LED_ALIGN_RIGHT)
        self._clock_display.SetValue("--.--.--")

        self.open_button = Button(self,
                                  -1,
                                  "Add",
                                  pos=(10, 125),
                                  size=(70, 35))
        self.open_button.SetBackgroundColour(Colour.DARK_GREEN)
        self.open_button.SetForegroundColour(Colour.WHITE)

        self.list_button = Button(self,
                                  -1,
                                  "List",
                                  pos=(10, 160),
                                  size=(70, 35))
        self.list_button.SetBackgroundColour(get_colour(0x333333))
        self.list_button.SetForegroundColour(Colour.WHITE)

        self.close_button = Button(self,
                                   -1,
                                   "Close",
                                   pos=(10, 195),
                                   size=(70, 35))
        self.close_button.SetBackgroundColour(Colour.DARK_RED)
        self.close_button.SetForegroundColour(Colour.WHITE)

        self._timer = Timer(self)
        self._timer.Start(100)
        self.Bind(EVT_TIMER, self.on_clock_update, self._timer)

    def set_display(self, value):
        """
        :param float value:
        """
        self._display.SetValue("{:.2f}".format(value))

    def on_clock_update(self, e):
        self._clock_display.SetValue(datetime.now().strftime("%H:%M:%S"))
        self._date_display.SetValue(datetime.now().strftime("%d-%m-%Y"))


class NumberInputWindow(Dialog):
    MAX_VALUE = 999999.99

    def __init__(self, parent, title=u"NumberInput"):
        Dialog.__init__(self,
                        parent,
                        title=title,
                        size=(320, 240),
                        style=BORDER_NONE)
        pnl = NumberInputWindowPanel(self)

        self.Bind(EVT_BUTTON, pnl.on_input_callback, pnl.keypad_0)
        self.Bind(EVT_BUTTON, pnl.on_input_callback, pnl.keypad_1)
        self.Bind(EVT_BUTTON, pnl.on_input_callback, pnl.keypad_2)
        self.Bind(EVT_BUTTON, pnl.on_input_callback, pnl.keypad_3)
        self.Bind(EVT_BUTTON, pnl.on_input_callback, pnl.keypad_4)
        self.Bind(EVT_BUTTON, pnl.on_input_callback, pnl.keypad_5)
        self.Bind(EVT_BUTTON, pnl.on_input_callback, pnl.keypad_6)
        self.Bind(EVT_BUTTON, pnl.on_input_callback, pnl.keypad_7)
        self.Bind(EVT_BUTTON, pnl.on_input_callback, pnl.keypad_8)
        self.Bind(EVT_BUTTON, pnl.on_input_callback, pnl.keypad_9)
        self.Bind(EVT_BUTTON, pnl.on_input_callback, pnl.keypad_00)

        self.Bind(EVT_BUTTON, pnl.on_delete, pnl.keypad_del)

        self.Bind(EVT_BUTTON, self.on_confirm, pnl.keypad_confirm)
        self.Bind(EVT_BUTTON, self.on_cancel, pnl.keypad_cancel)

        self.pnl = pnl

        # self._set_panel(pnl)
        self._sizer = BoxSizer()
        self._sizer.Clear()
        self._sizer.Add(self.pnl)
        self.SetSizer(self._sizer)

    def on_confirm(self, e):
        self.pnl.on_confirm(None)
        self.EndModal(ID_OK)

    def on_cancel(self, e):
        self.pnl.on_cancel(None)
        self.EndModal(ID_CANCEL)

    def get_result(self):
        return self.pnl.get_result()

    def get_value(self):
        return self.pnl.get_value()


class NumberInputWindowPanel(BaseWindowPanel):
    def __init__(self, parent):
        BaseWindowPanel.__init__(self,
                                 parent,
                                 bg_color=Colour.BLACK,
                                 fg_color=Colour.WHITE)

        self._display = LEDNumberCtrl(self,
                                      pos=(0, 0),
                                      size=(320, 70),
                                      style=LED_ALIGN_RIGHT)
        self._display.SetValue("0.00")

        self.keypad_7 = Button(self, -1, "7", size=(50, 50), pos=(5, 80))
        self.keypad_8 = Button(self, -1, "8", size=(50, 50), pos=(60, 80))
        self.keypad_9 = Button(self, -1, "9", size=(50, 50), pos=(115, 80))

        self.keypad_4 = Button(self, -1, "4", size=(50, 50), pos=(5, 130))
        self.keypad_5 = Button(self, -1, "5", size=(50, 50), pos=(60, 130))
        self.keypad_6 = Button(self, -1, "6", size=(50, 50), pos=(115, 130))

        self.keypad_1 = Button(self, -1, "1", size=(50, 50), pos=(5, 180))
        self.keypad_2 = Button(self, -1, "2", size=(50, 50), pos=(60, 180))
        self.keypad_3 = Button(self, -1, "3", size=(50, 50), pos=(115, 180))

        self.keypad_del = Button(self, -1, "<<", size=(50, 50), pos=(170, 80))
        self.keypad_0 = Button(self, -1, "00", size=(50, 50), pos=(170, 130))
        self.keypad_00 = Button(self, -1, "0", size=(50, 50), pos=(170, 180))

        self.keypad_cancel = Button(self, -1, "X", size=(75, 50), pos=(230, 80))
        self.keypad_confirm = Button(self, -1, "OK", size=(75, 100), pos=(230, 130))

        f = Font(20, FONTFAMILY_DEFAULT, FONTSTYLE_NORMAL, FONTWEIGHT_NORMAL)

        for b in [self.keypad_0,
                  self.keypad_1,
                  self.keypad_2,
                  self.keypad_3,
                  self.keypad_4,
                  self.keypad_5,
                  self.keypad_6,
                  self.keypad_7,
                  self.keypad_8,
                  self.keypad_9,
                  self.keypad_00]:  # type: Button
            b.SetBackgroundColour(get_colour(0x333333))
            b.SetForegroundColour(Colour.WHITE)
            b.SetFont(f)

        self.keypad_del.SetBackgroundColour(Colour.DARK_RED)
        self.keypad_del.SetForegroundColour(Colour.WHITE)
        self.keypad_del.SetFont(f)

        self.keypad_cancel.SetBackgroundColour(Colour.DARK_RED)
        self.keypad_cancel.SetForegroundColour(Colour.WHITE)
        self.keypad_cancel.SetFont(f)

        self.keypad_confirm.SetBackgroundColour(Colour.DARK_GREEN)
        self.keypad_confirm.SetForegroundColour(Colour.WHITE)
        self.keypad_confirm.SetFont(f)

        self._value = 0
        self._result_confirm = False

        self.set_value(0.00)

    def get_result(self):
        return self.get_value() if self._result_confirm else None

    def get_value(self):
        return float("{:.2f}".format(self._value))

    def set_value(self, value):
        self._value = value
        self._update_value()

    def add_value(self, value):
        v = int(value)
        val = self._value * 10

        if v == 0 and value == "00":
            val = val * 10
        else:
            val += (v * 0.01)

        if val > NumberInputWindow.MAX_VALUE:
            return

        self._value = val
        self._update_value()

    def delete_value(self, it=1):
        for i in range(it):
            v = float("{:.2f}".format(self._value)) * 100
            v -= (v % 10)  # Remove last digit
            self.set_value(v / 1000)

    def _update_value(self):
        self._display.SetValue("{:0.2f}".format(self._value))

    def on_input_callback(self, e):
        """
        :param CommandEvent e:
        :return:
        """
        o = e.GetEventObject()
        self.add_value(o.GetLabel())

    def on_delete(self, e):
        self.delete_value()

    def on_confirm(self, e):
        self._result_confirm = True
        # self.GetParent().Close()

    def on_cancel(self, e):
        # self.GetParent().Close()
        pass

    # @Override
    def Show(self, show=True):
        self._result_confirm = False
        super(NumberInputWindowPanel, self).Show(show)
        self.set_value(0)


class CategoryInputWindow(Dialog):
    def __init__(self, parent, title=u"Categories", categories=[]):
        Dialog.__init__(self,
                        parent,
                        title=title,
                        size=(320, 240),
                        style=BORDER_NONE)
        pnl = CategoryInputWindowPanel(self, title, categories)

        self.pnl = pnl
        self._sizer = BoxSizer()
        self._sizer.Clear()
        self._sizer.Add(self.pnl)
        self.SetSizer(self._sizer)

    def get_value(self):
        return self.pnl.get_value()


class CategoryInputWindowPanel(BaseWindowPanel):
    EMPTY_ITEM = '<empty>'

    def __init__(self, parent, title, categories):
        BaseWindowPanel.__init__(self,
                                 parent,
                                 bg_color=Colour.BLACK,
                                 fg_color=Colour.WHITE)

        # Title Label
        self._title_label = StaticText(self,
                                       pos=(85, 10),
                                       size=(100, 30),
                                       label=title)
        self._title_label.SetFont(Font(20, FONTFAMILY_DEFAULT, FONTSTYLE_NORMAL, FONTWEIGHT_NORMAL))

        # Cancel Button
        self._cancel_button = Button(self,
                                     -1,
                                     "Cancel",
                                     pos=(10, 10),
                                     size=(70, 30))
        self._cancel_button.SetBackgroundColour(Colour.DARK_RED)
        self._cancel_button.SetForegroundColour(Colour.WHITE)

        # Confirm Button
        self._confirm_button = Button(self,
                                      -1,
                                      "OK",
                                      pos=(240, 10),
                                      size=(70, 30))
        self._confirm_button.SetBackgroundColour(Colour.DARK_GREEN)
        self._confirm_button.SetForegroundColour(Colour.WHITE)

        # List Views
        self._list_control = ListBox(self,
                                     pos=(10, 50),
                                     size=(295, 170))
        self._list_control.SetBackgroundColour(Colour.BLACK)
        self._list_control.SetForegroundColour(Colour.WHITE)
        self._list_control.SetItems([CategoryInputWindowPanel.EMPTY_ITEM] + categories)

        # Event
        self.Bind(EVT_BUTTON, self._confirm_button_click, self._confirm_button)
        self.Bind(EVT_BUTTON, self._cancel_button_click, self._cancel_button)

    def _cancel_button_click(self, e):
        self.GetParent().EndModal(ID_CANCEL)

    def _confirm_button_click(self, e):
        self.GetParent().EndModal(ID_OK)

    def get_value(self):
        v = self._list_control.GetStringSelection()
        return "" if v == CategoryInputWindowPanel.EMPTY_ITEM else v
