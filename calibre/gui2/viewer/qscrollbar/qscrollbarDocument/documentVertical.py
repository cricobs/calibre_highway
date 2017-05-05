from calibre.gui2.viewer.qscrollbar.qscrollbar import Qscrollbar


class DocumentVertical(Qscrollbar):
    def __init__(self, *args, **kwargs):
        super(DocumentVertical, self).__init__(*args, **kwargs)

    @property
    def mode_view(self):
        return True

    def on_topLevelWidget_iteratorChanged(self, ebookiterator):
        self.setMinimum(100)
        self.setMaximum(100 * sum(ebookiterator.pages))
        self.setSingleStep(10)
        self.setPageStep(100)
        self.set_value(1)

    def set_value(self, value):
        self.blockSignals(True)
        self.setValue(int(value * 100))
        self.blockSignals(False)
