from calibre.gui2.viewer.qlineedit.qlineedit import Qlineedit


class QlineeditSearchReplace(Qlineedit):
    def __init__(self, *args, **kwargs):
        super(QlineeditSearchReplace, self).__init__(*args, **kwargs)

        # completer = self.completer()
        # completer.setCompletionMode(completer.PopupCompletion)
