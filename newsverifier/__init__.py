from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QAction, QLabel, QMenu, QMenuBar, QToolBar, QMainWindow, QVBoxLayout
from PyQt5.QtGui import QFont, QIcon

from newsverifier import qrc_resources

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("Fake News Detector")
        self.setGeometry(100, 100, 1024, 768)

        self.viewWidget = ViewWidget(self)
        self.setCentralWidget(self.viewWidget)
        self._createActions()
        self._createMenuBar()
        self._createToolsBar()

    def _createActions(self):
        self.openAction = QAction("&Open...", self)
        self.exitAction = QAction("&Exit", self)
        self.copyAction = QAction("&Copy", self)
        self.pasteAction = QAction("&Paste", self)
        self.cutAction = QAction("C&ut", self)
        self.aboutAction = QAction("&About", self)
        self.helpContentAction = QAction("&Help Content", self)
        self.verifyAction = QAction(QIcon(":verify.svg"),"&Verify", self)
        self.undoAction = QAction(QIcon(":undo.svg"), "&Undo", self)
        self.redoAction = QAction(QIcon(":redo.svg"), "&Redo...", self)

    
    def _createMenuBar(self):
        menuBar = QMenuBar(self)
        self.setMenuBar(menuBar)

        fileMenu = QMenu("&File", self)
        menuBar.addMenu(fileMenu)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.exitAction)

        editMenu = QMenu("&Edit", self)
        menuBar.addMenu(editMenu)
        editMenu.addAction(self.copyAction)
        editMenu.addAction(self.pasteAction)
        editMenu.addAction(self.cutAction)

        helpMenu = QMenu("&Help", self)
        menuBar.addMenu(helpMenu)
        helpMenu.addAction(self.helpContentAction)
        helpMenu.addAction(self.aboutAction)
    
    def _createToolsBar(self):
        mainToolBar = QToolBar("Verify", self)
        self.addToolBar(Qt.TopToolBarArea, mainToolBar)
        mainToolBar.addAction(self.undoAction)
        mainToolBar.addAction(self.redoAction)
        mainToolBar.addAction(self.verifyAction)


class ViewWidget(QWidget):
    def __init__(self, parent):
        super(ViewWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.initializeUI()
        self.setLayout(self.layout)

    def initializeUI(self):
        self.displayLabels()
    
    def displayLabels(self):
        self.text = QLabel(self)
        self.text.setText("Fake News Detector")
        self.text.setFont(QFont("Roboto", 16))
        self.layout.addWidget(self.text)


        