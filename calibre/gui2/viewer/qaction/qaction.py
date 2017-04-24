from PyQt5.QtWidgets import QAction


class Qaction(QAction):
    def __init__(self, *args, **kwargs):
        super(Qaction, self).__init__(*args, **kwargs)

        self.group = None
        self.parents = []

    def set_data(self, name, value):
        data = self.data()
        data[name] = value

        self.setData(data)
