from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

from calibre.gui2.viewer.library.exception import PropertyException
from calibre.gui2.viewer.qaction.qaction import Qaction
from calibre.gui2.viewer.qobject.qobject import Qobject


class Qwidget(QWidget, Qobject):
    visibilityChanged = pyqtSignal(bool)
    NONE, SEARCH, REPLACE, ALL = list(map(lambda x: 2 ** x, range(4)))

    def __init__(self, *args, **kwargs):
        super(Qwidget, self).__init__(*args, **kwargs)

        if self.mode_search ^ self.NONE:
            self.qapplication.search.connect(self.on_qapplication_search)
            self.qapplication.replace.connect(self.on_qapplication_replace)
        if self.mode_save:
            self.qapplication.aboutToQuit.connect(self.on_qapplication_aboutToQuit)
        if self.mode_selection:
            self.selectionChanged.connect(self.qapplication.selectionChanged)
            self.selectionChanged.connect(self.qapplication.on_qwidget_selectionChanged)
        if self.mode_view:
            self.qapplication.topLevelWidget().iteratorChanged.connect(
                self.on_topLevelWidget_iteratorChanged)
        if self.mode_toggle:
            self.qaction_toggle = Qaction(self)
            self.qaction_toggle.triggered.connect(self.on_qaction_toggle_triggered)

            q = getattr(self, "toggleViewAction", None)
            if q:
                q = q()
                self.qaction_toggle.setCheckable(True)
                self.qaction_toggle.setChecked(q.isChecked())
                self.qaction_toggle.triggered.connect(q.trigger)
                self.qaction_toggle.setText(q.text())

    def show_parents(self):
        self.show()
        try:
            self.parent().show_parents()
        except AttributeError:
            pass

    @property
    def visible(self):
        return self.isVisible()

    def on_topLevelWidget_iteratorChanged(self, ebookiterator):
        """
        called if mode_view
        :param ebookiterator:
        :return:
        """
        pass

    @property
    def mode_view(self):
        """
        connect qapplication.topLevelWidget().iteratorChanged to on_topLevelWidget_iteratorChanged
        :return:
        """
        return False

    @property
    def selected_text(self):
        """
        called in qapplication.selectedText() if mode_selection
        :return:
        """
        if self.mode_selection:
            raise PropertyException

    @property
    def mode_selection(self):
        """
        connect selectionChanged to qapplication.selectionChanged
        :return:
        """
        return False

    def _addAction(self, action):
        """
        reimplementation of overload addAction(action)
        :param action:
        :return:
        """
        separator = getattr(action, "separator", None)
        data = action.data() or {}
        position = data.get("position", None)
        if position is not None:
            actions = self.actions()
            for i, a in enumerate(actions):
                d = a.data() or {}
                p = d.get("position", None)
                if p > position:
                    self.insertAction(a, action)
                    if separator:
                        self.insertSeparator(a)

                    return

        super(Qwidget, self).addAction(action)
        if separator:
            self.addSeparator()

    def setWindowTitle(self, p_str):
        super(Qwidget, self).setWindowTitle(p_str)

        if self.mode_toggle:
            try:
                self.qaction_toggle.setText(p_str)
            except AttributeError:
                pass

    @property
    def mode_toggle(self):
        """
        connect qaction_toggle to on_qaction_toggle_triggered
        :return:
        """
        return False

    def on_qaction_toggle_triggered(self, checked):
        """
        called if getattr(self, "toggleViewAction")
        :param checked:
        :return:
        """
        pass

    def on_qapplication_aboutToQuit(self):
        """
        called if self.mode_save
        :return:
        """
        pass

    def search(self, search, backwards=False):
        """
        called on_qapplication_search
        :param search:
        :param backwards:
        :return:
        """
        pass

    def replace(self, search, replace, backwards=False):
        """
        called on on_qapplication_replace
        :param search:
        :param replace:
        :param backwards:
        :return:
        """
        pass

    def on_qapplication_search(self, qwidget, search, backwards):
        """
        called if mode_search ^ self.NONE
        :param qwidget:
        :param search:
        :param backwards:
        :return:
        """
        if qwidget is self:
            self.search(search, backwards)

    def on_qapplication_replace(self, qwidget, search, replace, backwards):
        """
        called if mode_search ^ self.NONE
        :param qwidget:
        :param search:
        :param replace:
        :param backwards:
        :return:
        """
        if qwidget is self:
            self.replace(search, replace, backwards)

    @property
    def mode_save(self):
        """
        connect on_qapplication_aboutToQuit
        :return:
        """
        return False

    @property
    def mode_visibility(self):
        """
        emit visibilityChanged
        :return:
        """
        return False

    @property
    def mode_search(self):
        """
        connect on_qapplication_replace, on_qapplication_search
        :return:
        """
        return self.NONE

    def visibility_changed(self, visibility):
        if self.mode_visibility:
            self.visibilityChanged.emit(visibility)

        if self.mode_toggle:
            self.qaction_toggle.setChecked(visibility)

    def hideEvent(self, qhideevent):
        super(Qwidget, self).hideEvent(qhideevent)

        self.visibility_changed(False)

    def showEvent(self, qshowevent):
        super(Qwidget, self).showEvent(qshowevent)

        self.visibility_changed(True)
