from PyQt5.QtWidgets import QDoubleSpinBox

from calibre.gui2.viewer.qwidget.qwidget import Qwidget


class Qdoublespinbox(QDoubleSpinBox, Qwidget):
    def __init__(self, *args, **kwargs):
        super(Qdoublespinbox, self).__init__(*args, **kwargs)