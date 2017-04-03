from calibre.gui2.viewer.qwebview.qwebview import Qwebview


class QwebviewFootnote(Qwebview):
    def __init__(self, *args, **kwargs):
        super(QwebviewFootnote, self).__init__(*args, **kwargs)