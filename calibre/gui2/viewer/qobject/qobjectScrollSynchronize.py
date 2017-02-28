from calibre.gui2.viewer.qobject.qobject import Qobject


class QobjectScrollSynchronize(Qobject):
    def __init__(self, *qwidgets, **kwargs):
        super(QobjectScrollSynchronize, self).__init__(**kwargs)
        self.p_position = None
        self.s_position = None

        # self.qwebviewPreview.page().scrollRequested.connect(
        #     self.on_qwebviewPreview_scrollRequested)
        # self.qplaintexteditSynopsis.verticalScrollBar().sliderMoved.connect(
        #     self.on_qplaintexteditSynopsis_sliderMoved) # fixme use scrollbar released
        #
    # def on_qplaintexteditSynopsis_sliderMoved(self, value):
    #     p_height = self.qwebviewPreview.page().mainFrame().scrollBarMaximum(Qt.Vertical)
    #     s_height = self.qplaintexteditSynopsis.verticalScrollBar().maximum()
    #
    #     s_position = self.qplaintexteditSynopsis.verticalScrollBar().sliderPosition()
    #     p_position = s_position * float(p_height) / s_height
    #
    #     self.qplaintexteditSynopsis.verticalScrollBar().blockSignals(True)
    #     self.qwebviewPreview.page().mainFrame().blockSignals(True)
    #     self.qwebviewPreview.page().mainFrame().setScrollPosition(QPoint(0, p_position))
    #     self.qwebviewPreview.page().mainFrame().blockSignals(False)
    #     self.qplaintexteditSynopsis.verticalScrollBar().blockSignals(False)
    #
    # def on_qwebviewPreview_scrollRequested(self, dx, dy, rectToScroll):
    #     p_height = self.qwebviewPreview.page().mainFrame().scrollBarMaximum(Qt.Vertical)
    #     s_height = self.qplaintexteditSynopsis.verticalScrollBar().maximum()
    #
    #     p_position = self.qwebviewPreview.page().mainFrame().scrollPosition().y()
    #     s_position = p_position * float(s_height) / p_height
    #
    #     QTimer().singleShot(111, lambda : self.update_edit(s_position))
    #
    # def update_edit(self, position):
    #     self.qplaintexteditSynopsis.verticalScrollBar().blockSignals(True)
    #     self.qwebviewPreview.page().mainFrame().blockSignals(True)
    #     self.qplaintexteditSynopsis.verticalScrollBar().setValue(position)
    #     self.qwebviewPreview.page().mainFrame().blockSignals(False)
    #     self.qplaintexteditSynopsis.verticalScrollBar().blockSignals(False)
