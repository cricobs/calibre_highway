from PyQt5.QtWidgets import QAction

from calibre.gui2.viewer.qmenu.qmenuDropdown import QmenuDropdown


class Qaction(QAction):
    def __init__(self, *args, **kwargs):
        super(Qaction, self).__init__(*args, **kwargs)

        self.group = None
        self.parents = []
        self.setData(None)
        self.qmenu = None

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

    def update(self, qmenu):
        """
        called on Qmenu.exec_
        :return:
        """
        self.qmenu = qmenu

        data = self.data() or {}
        if data.get("text_format", None):
            text = self.qmenu.selected_text
            text = text[:22] + (text[22:] and '...')

            self.setText(self.data().get("text_format").format(text))
