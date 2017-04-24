from PyQt5.QtWidgets import QAction


class Qaction(QAction):
    def __init__(self, *args, **kwargs):
        super(Qaction, self).__init__(*args, **kwargs)

        self.group = None
        self.parents = []
        self.setData(None)

    def setData(self, data):
        return super(Qaction, self).setData(data or {})

    def set_data(self, name, value):
        data = self.data()
        data[name] = value

        self.setData(data)

    def create_qmenu(self):
        from calibre.gui2.viewer.qmenu.qmenu import Qmenu

        qmenu = Qmenu()
        self.setMenu(qmenu)

        return qmenu

    def update(self):
        """
        called on Qmenu.exec_
        :return:
        """
        if self.objectName() == "qaction_search_online":
            self.set_text_format(self.parent().selected_text)

    def set_text_format(self, *args, **kwargs):
        self.setText(self.data().get("text_format").format(*args, **kwargs))
