from PyQt5.QtCore import pyqtSignal

from calibre.gui2.viewer.qdoublespinbox.qdoublespinbox import Qdoublespinbox


class QdoublespinboxPosition(Qdoublespinbox):
    positionChanged = pyqtSignal(object, object)
    goToPosition = pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super(QdoublespinboxPosition, self).__init__(*args, **kwargs)

        self.tt = _('Position in book')
        self.setToolTip(self.tt)
        self.editingFinished.connect(lambda: self.goToPosition.emit(self.value()))

    @property
    def mode_view(self):
        return True

    def on_topLevelWidget_iteratorChanged(self, ebookiterator):
        pages = sum(ebookiterator.pages)
        self.setMaximum(pages)
        self.setSuffix(' / %d' % pages)

    def set_value(self, val):
        self.blockSignals(True)
        self.setValue(val)
        try:
            self.setToolTip(self.tt + ' [{0:.0%}]'.format(float(val) / self.maximum()))
        except ZeroDivisionError:
            self.setToolTip(self.tt)

        self.blockSignals(False)
        self.update_value()

    def update_value(self):
        self.positionChanged.emit(self.value(), self.maximum())
