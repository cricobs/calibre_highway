from calibre.gui2.viewer.qdockwidget.qdockwidget import Qdockwidget


class QdockwidgetContent(Qdockwidget):
    def __init__(self, *args, **kwargs):
        super(QdockwidgetContent, self).__init__(*args, **kwargs)

        self.qwidgetSearch.toc_view = self.qtreeviewContent
