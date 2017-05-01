from calibre.gui2.viewer.qwebpage.qwebpageFootnote import QwebpageFootnote
from calibre.gui2.viewer.qwebview.qwebview import Qwebview


class QwebviewFootnote(Qwebview):
    def __init__(self, *args, **kwargs):
        super(QwebviewFootnote, self).__init__(*args, **kwargs)

    def create_page(self):
        return QwebpageFootnote(self)
