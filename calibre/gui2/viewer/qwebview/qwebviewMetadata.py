from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QPalette

from calibre.gui2 import rating_font
from calibre.gui2.viewer.qwebview.qwebview import Qwebview
from calibre.utils.localization import is_rtl


class QwebviewMetadata(Qwebview):
    def __init__(self, *args, **kwargs):
        super(QwebviewMetadata, self).__init__(*args, **kwargs)

        s = self.settings()
        s.setAttribute(s.JavascriptEnabled, False)

        palette = self.palette()
        palette.setBrush(QPalette.Base, Qt.transparent)
        self.page().setPalette(palette)
        self.page().setLinkDelegationPolicy(self.page().DelegateAllLinks)

        self.setAttribute(Qt.WA_OpaquePaintEvent, False)
        self.setVisible(False)

        self.window().installEventFilter(self)

    def eventFilter(self, qobject, qevent):
        if qevent.type() == qevent.KeyPress:
            if qevent.key() == Qt.Key_Escape:
                if self.isVisible():
                    self.setVisible(False)
        elif qevent.type() == qevent.Resize:
            if self.isVisible():
                self.update_layout()

        return super(QwebviewMetadata, self).eventFilter(qobject, qevent)

    def update_layout(self):
        self.setGeometry(0, 0, self.parent().width(), self.parent().height())

    def show_metadata(self, mi, ext=''):
        from calibre.gui2.book_details import render_html, css
        from calibre.ebooks.metadata.book.render import mi_to_html

        def render_data(mi, use_roman_numbers=True, all_fields=False):
            return mi_to_html(mi, use_roman_numbers=use_roman_numbers, rating_font=rating_font(),
                              rtl=is_rtl())

        html = render_html(mi, css(), True, self, render_data_func=render_data)
        self.setHtml(html)

    def setVisible(self, x):
        if x:
            self.update_layout()

        super(QwebviewMetadata, self).setVisible(x)

    def paintEvent(self, ev):
        p = QPainter(self)
        p.fillRect(ev.region().boundingRect(), QBrush(QColor(200, 200, 200, 220), Qt.SolidPattern))
        p.end()

        super(QwebviewMetadata, self).paintEvent(ev)
