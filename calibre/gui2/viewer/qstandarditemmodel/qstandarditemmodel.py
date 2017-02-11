from PyQt5.QtGui import QStandardItemModel


class Qstandarditemmodel(QStandardItemModel):
    def __init__(self, *args, **kwargs):
        super(Qstandarditemmodel, self).__init__(*args)
