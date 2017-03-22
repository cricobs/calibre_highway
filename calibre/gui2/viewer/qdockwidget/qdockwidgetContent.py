from calibre.gui2.viewer.qdockwidget.qdockwidget import Qdockwidget


class QdockwidgetContent(Qdockwidget):
    def __init__(self, *args, **kwargs):
        super(QdockwidgetContent, self).__init__(*args, **kwargs)

        self.qwidgetSearch.toc_view = self.qtreeviewContent

    def raise_(self):
        super(QdockwidgetContent, self).raise_()
        index = self.qtreeviewContent.model().currently_viewed_entry.index()
        self.qtreeviewContent.scrollTo(index, self.qtreeviewContent.PositionAtTop)

