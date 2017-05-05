from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QApplication

from calibre.gui2.viewer.library.thing import property_setter
from calibre.gui2.viewer.qmenu.qmenuDropdown import QmenuDropdown


class Qaction(QAction):
    visibilityChanged = pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        super(Qaction, self).__init__(*args, **kwargs)

        self.group = None
        self.parents = []
        self.setData(None)
        self.qmenu = None

    @pyqtSlot(bool)
    def set_visible(self, visible):
        self.visible = visible

    @property_setter
    def visible(self, visible):
        self.visibilityChanged.emit(visible)

    def setData(self, data):
        return super(Qaction, self).setData(data if data is not None else {})

    def set_data(self, name, value):
        data = self.data()
        data[name] = value

        self.setData(data)

    def create_qmenu(self):
        qmenu = QmenuDropdown(None)
        self.setMenu(qmenu)

        return qmenu

    def update(self):
        """
        called on Qmenu.exec_
        :return:
        """
        data = self.data() or {}
        if data.get("text_format", None):
            text = QApplication.instance().selected_text()
            text = text[:22] + (text[22:] and '...')

            self.setText(self.data().get("text_format").format(text))
