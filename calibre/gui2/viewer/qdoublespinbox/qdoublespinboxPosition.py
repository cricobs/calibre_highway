from PyQt5.QtCore import pyqtSignal

from calibre.gui2.viewer.qdoublespinbox.qdoublespinbox import Qdoublespinbox


class QdoublespinboxPosition(Qdoublespinbox):
    value_changed = pyqtSignal(object, object)

    def __init__(self, *args, **kwargs):
        super(QdoublespinboxPosition, self).__init__(*args, **kwargs)

        self.tt = _('Position in book')
        self.setToolTip(self.tt)

    def set_value(self, val):
        self.blockSignals(True)
        self.setValue(val)
        try:
            self.setToolTip(self.tt +
                            ' [{0:.0%}]'.format(float(val) / self.maximum()))
        except ZeroDivisionError:
            self.setToolTip(self.tt)
        self.blockSignals(False)
        self.value_changed.emit(self.value(), self.maximum())
