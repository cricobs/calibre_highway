from calibre.gui2.viewer.qscrollbar.qscrollbarDocument.document import Document


class DocumentHorizontal(Document):
    def __init__(self, *args, **kwargs):
        super(DocumentHorizontal, self).__init__(*args, **kwargs)

    def setVisible(self, visible):
        self.blockSignals(True)
        if visible > 0:
            self.setRange(0, visible)
            self.setValue(0)
            self.setSingleStep(1)
            self.setPageStep(int(visible / 10.))

        super(DocumentHorizontal, self).setVisible(visible > 0)
        self.blockSignals(False)
