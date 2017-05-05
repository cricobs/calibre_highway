from calibre.gui2.viewer.qscrollbar.qscrollbar import Qscrollbar


class Document(Qscrollbar):
    def __init__(self, *args, **kwargs):
        super(Document, self).__init__(*args, **kwargs)