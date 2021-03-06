from calibre.gui2.viewer.qlabel.qlabelClock import QlabelClock
from calibre.gui2.viewer.qlabel.qlabelPosition import QlabelPosition
from calibre.gui2.viewer.qwebview.qwebviewMetadata import QwebviewMetadata
from calibre.gui2.viewer.qwidget.qwidget import Qwidget
from calibre.gui2.viewer.qwidget.qwidgetProgress import QwidgetProgress


class QwidgetDocument(Qwidget):
    def __init__(self, *args, **kwargs):
        super(QwidgetDocument, self).__init__(*args, **kwargs)

        self.qwebviewMetadata = QwebviewMetadata(self)

        self.qwidgetProgress = QwidgetProgress(self)

        self.qlabelPosition = QlabelPosition(self)
        self.qlabelPosition.set_style_options('rgba(0, 0, 0, 0)', self.view.qwebpage.colors()[1])
        self.qlabelPosition.mode_fullscreen = self.view.qwebpage.fullscreen_scrollbar

        self.qlabelClock = QlabelClock(self)
        self.qlabelClock.set_style_options('rgba(0, 0, 0, 0)', self.view.qwebpage.colors()[1])
        self.qlabelClock.setEnabled(self.view.qwebpage.fullscreen_clock)

        self.qwidgetSearch.pos.positionChanged.connect(self.qlabelPosition.update_value)
        self.qwidgetSearch.pos.positionChanged.connect(self.vertical_scrollbar.set_value)

        self.window().setCentralWidget(self)
        self.window().iteratorChanged.connect(self.on_window_iteratorChanged)

    def on_window_iteratorChanged(self, iterator):
        self.qwebviewMetadata.show_metadata(iterator.mi, iterator.book_format)
