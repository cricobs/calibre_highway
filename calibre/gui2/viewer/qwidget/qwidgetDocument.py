from calibre.gui2.viewer.qwebview.qwebviewMetadata import QwebviewMetadata
from calibre.gui2.viewer.qwidget.qwidget import Qwidget


class QwidgetDocument(Qwidget):
    def __init__(self, *args, **kwargs):
        super(QwidgetDocument, self).__init__(*args, **kwargs)

        self.qwebviewMetadata = QwebviewMetadata(self)

        self.window().setCentralWidget(self)
        self.window().ebookLoaded.connect(self.on_window_ebookLoaded)

    def on_window_ebookLoaded(self, iterator):
        self.qwebviewMetadata.show_metadata(iterator.mi, iterator.book_format)
