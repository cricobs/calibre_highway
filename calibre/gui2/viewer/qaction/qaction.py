from PyQt5.QtWidgets import QAction


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
        from calibre.gui2.viewer.qmenu.qmenu import Qmenu

        qmenu = Qmenu()
        self.setMenu(qmenu)

        return qmenu

    def update(self, qmenu=None, text_format=None):
        """
        called on Qmenu.exec_
        :return:
        """
        self.qmenu = qmenu

        if self.objectName() in ["qaction_search_online"]:
            self.set_text_format(text_format[:22] + (text_format[22:] and '...'))

    def set_text_format(self, *args, **kwargs):
        self.setText(self.data().get("text_format").format(*args, **kwargs))
