from PyQt5.QtWebKitWidgets import QWebPage

from calibre.gui2.viewer.qobject.qobject import Qobject


class Qwebpage(QWebPage, Qobject):
    def __init__(self, *args, **kwargs):
        super(Qwebpage, self).__init__(*args, **kwargs)

        # self.setLinkDelegationPolicy(self.DelegateAllLinks)
        self.settings().setAttribute(self.settings().DeveloperExtrasEnabled, True)
