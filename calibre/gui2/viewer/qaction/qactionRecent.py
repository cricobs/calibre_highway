import os

from calibre.gui2.viewer.qaction.qaction import Qaction


class QactionRecent(Qaction):
    def __init__(self, path, parent):
        self.path = path
        super(QactionRecent, self).__init__(os.path.basename(path), parent)
