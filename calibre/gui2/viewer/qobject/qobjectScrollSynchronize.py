from calibre.gui2.viewer.qobject.qobject import Qobject


class QobjectScrollSynchronize(Qobject):
    def __init__(self, *qwidgets, **kwargs):
        super(QobjectScrollSynchronize, self).__init__(**kwargs)
