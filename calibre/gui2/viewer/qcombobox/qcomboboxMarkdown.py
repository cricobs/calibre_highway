from calibre.gui2.viewer.qcombobox.qcombobox import Qcombobox


class QcomboboxMarkdown(Qcombobox):
    def __init__(self, *args, **kwargs):
        super(QcomboboxMarkdown, self).__init__(*args, **kwargs)

        self.addItem("Format")
