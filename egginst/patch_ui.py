from os.path import basename, dirname, join
import sys

from PyQt4 import QtCore, QtGui, uic     

# Translation function
def tr(context, text):
    return QtGui.QApplication.translate(context, text, None, QtGui.QApplication.UnicodeUTF8)


class PatcherApp(QtGui.QApplication):
    def __init__(self, patches=[], patch_fn=None, translation_file=None):
        super(PatcherApp, self).__init__(sys.argv)
        
        self._load_translations(translation_file)
        self._register_event_types()
        self._open_status_window()
        self._start_patch_thread(patches, patch_fn)

    def _load_translations(self, translation_file):
        if translation_file:
            # Load the app-specific translation resources.
            translator = QtCore.QTranslator()
            translator.load(basename(translation_file), dirname(translation_file))
            self.installTranslator(translator)

    def _open_status_window(self):
        self.window = StatusWidget()
        self.window.show()
        self.window.raise_()

    def _register_event_types(self):
        # Register the event type(s) that will be used
        _InsertEggEvent.EVENT_TYPE = QtCore.QEvent.registerEventType(_InsertEggEvent.EVENT_TYPE)

    def _start_patch_thread(self, patches, patch_fn):
        self.thread = _PatchThread(patches, patch_fn, self.window)
        self.thread.finished.connect(self._thread_finished)
        self.thread.start()
    
    def _thread_finished(self):
        self.exit()


class StatusWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(StatusWidget, self).__init__(parent)
        
        # Load the UI and make sure it's translated
        form_class, wc = uic.loadUiType(join(dirname(__file__), "patch_ui.ui"))
        self.form = form_class()
        self.form.setupUi(self)
        if self.form is not None:
            self.form.retranslateUi(self)

    def customEvent(self, event):
        if event.type() == _InsertEggEvent.EVENT_TYPE:
            # Note the egg that is being installed
            status = unicode(tr("UpdateStatusWidget", "Installing: %1").arg(basename(event.path())))
            self.form.status_message.setText(status)
            self.form.progress_bar.setValue(event.percentage())
            event.accept()
        else:
            event.ignore()


class _InsertEggEvent(QtCore.QEvent):
    EVENT_TYPE = QtCore.QEvent.User
    
    def __init__(self, path, percentage):
        super(_InsertEggEvent, self).__init__(_InsertEggEvent.EVENT_TYPE)
        self._path = path
        self._percentage = percentage
    
    def path(self):
        return self._path
    
    def percentage(self):
        return self._percentage * 100.0


class _PatchThread(QtCore.QThread):
    def __init__(self, patches, patch_fn, window, parent=None):
        super(_PatchThread, self).__init__(parent)

        self.patches = patches
        self.apply_patch = patch_fn
        self.window = window

    def run(self):
        count = len(self.patches)
        for i, patch in enumerate(self.patches):
            QtGui.QApplication.instance().postEvent(self.window,
                                                    _InsertEggEvent(patch, (i+1)/float(count)))
            self.apply_patch(patch)

