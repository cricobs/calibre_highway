from calibre.gui2.viewer.qdockwidget.qdockwidget import Qdockwidget


class QdockwidgetContent(Qdockwidget):
    def __init__(self, *args, **kwargs):
        super(QdockwidgetContent, self).__init__(*args, **kwargs)

    def search(self, search, backwards=False):
        self.qtreeviewContent.search(search, backwards=backwards)

    @property
    def qwidgettitlebar(self):
        return self.titleBarWidget()

    @property
    def mode_hide(self):
        return True

    @property
    def mode_search(self):
        return self.SEARCH
