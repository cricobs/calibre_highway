from calibre.gui2.viewer.qdockwidget.qdockwidget import Qdockwidget


class QdockwidgetContent(Qdockwidget):
    def __init__(self, *args, **kwargs):
        super(QdockwidgetContent, self).__init__(*args, **kwargs)

        self.qwidgetSearch.toc_view = self.qtreeviewContent

    @property
    def mode_hide(self):
        return True

    def raise_(self):
        super(QdockwidgetContent, self).raise_()
        entry = self.qtreeviewContent.model().currently_viewed_entry
        if not entry:
            return

        self.qtreeviewContent.scrollTo(entry.index(), self.qtreeviewContent.PositionAtTop)

