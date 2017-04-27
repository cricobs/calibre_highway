from calibre.gui2.viewer.qdockwidget.qdockwidget import Qdockwidget
from calibre.gui2 import error_dialog


class QdockwidgetContent(Qdockwidget):
    def __init__(self, *args, **kwargs):
        super(QdockwidgetContent, self).__init__(*args, **kwargs)

    def search(self, search, backwards=False):
        # fixme use direction
        index = self.qtreeviewContent.model().search(search)
        if index.isValid():
            self.qtreeviewContent.searched.emit(index)
        else:
            error_dialog(
                self.qtreeviewContent, 'No matches found',
                'There are no Table of Contents entries matching: ' + search, show=True)

    @property
    def qwidgettitlebar(self):
        return self.titleBarWidget()

    @property
    def mode_hide(self):
        return True

    @property
    def mode_search(self):
        return self.SEARCH

    def raise_(self):
        super(QdockwidgetContent, self).raise_()
        entry = self.qtreeviewContent.model().currently_viewed_entry
        if not entry:
            return

        self.qtreeviewContent.scrollTo(entry.index(), self.qtreeviewContent.PositionAtTop)
