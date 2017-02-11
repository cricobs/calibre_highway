from calibre.gui2.viewer.qwebview.qwebview import Qwebview


class QwebviewPreview(Qwebview):
    def __init__(self, *args, **kwargs):
        super(QwebviewPreview, self).__init__(*args, **kwargs)