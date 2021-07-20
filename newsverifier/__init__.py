import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QAction, QLabel, QMenu, QMenuBar, QToolBar, QStatusBar, QMainWindow, QTextEdit, QVBoxLayout
from PyQt5.QtGui import QFont, QIcon

from newsverifier import qrc_resources


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("Fake News Detector")
        self.setGeometry(100, 100, 1024, 768)
        self.charCountNum = 0
        self.wordCountNum = 0
        self.viewWidget = ViewWidget(self)
        self.viewWidget.editor.textChanged.connect(self.calcStats)
        self.setCentralWidget(self.viewWidget)
        self._createActions()
        self._createMenuBar()
        self._createToolsBar()
        self._createStatusBar()
    
    def calcStats(self):
        wordcount = len(self.viewWidget.editor.toPlainText().split(' '))
        charcount = len(self.viewWidget.editor.toPlainText())

        self.charCountNum = charcount
        self.wordCountNum = wordcount

        


    def _createActions(self):
        self.openAction = QAction("&Open File", self)
        self.exitAction = QAction("&Exit", self)
        self.copyAction = QAction("&Copy", self)
        self.pasteAction = QAction("&Paste", self)
        self.cutAction = QAction("C&ut", self)
        self.aboutAction = QAction("&About", self)
        self.helpContentAction = QAction("&Help Content", self)
        self.verifyAction = QAction(QIcon(":verify.svg"),"&Verify", self)
        self.verifyAction.triggered.connect(self.makeVerification)
        self.undoAction = QAction(QIcon(":undo.svg"), "&Undo", self)
        self.undoAction.triggered.connect(self.makeUndo)
        self.redoAction = QAction(QIcon(":redo.svg"), "&Redo...", self)
        self.redoAction.triggered.connect(self.makeRedo)
    
    def makeUndo(self):
        editor = self.viewWidget.editor
        editor.undo()
    
    def makeRedo(self):
        editor = self.viewWidget.editor
        editor.redo()
    
    def makeVerification(self):
        text = self.viewWidget.editor.toPlainText()
        if(text):
            response =  predict(text)
        else:
            pass

    def _createMenuBar(self):
        menuBar = QMenuBar(self)
        self.setMenuBar(menuBar)

        fileMenu = QMenu("&File", self)
        menuBar.addMenu(fileMenu)
        fileMenu.addAction(self.openAction)
        fileMenu.addSeparator()
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
        mainToolBar.setMovable(False)
        mainToolBar.addAction(self.undoAction)
        mainToolBar.addAction(self.redoAction)
        mainToolBar.addAction(self.verifyAction)
    
    def _createStatusBar(self):
        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)

        self.charCountVar = QLabel(f"{ self.charCountNum } Characters")
        self.wordCountVar = QLabel(f"{ self.wordCountNum } Words")
        self.statusbar.addPermanentWidget(self.charCountVar)
        self.statusbar.addPermanentWidget(self.wordCountVar)


class ViewWidget(QWidget):
    def __init__(self, parent):
        super(ViewWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.setEditor()
        self.setLayout(self.layout)
    
    def setEditor(self):
        self.editor = QTextEdit(self)
        self.layout.addWidget(self.editor)


import torch
import pandas as pd

from newsverifier.utils.custpickle import CustomUnpickler
from newsverifier.utils.preprocess import preprocess

current_wd = os.getcwd()
model = CustomUnpickler( open(f'{current_wd}/newsverifier/data/multi-layer-perceptron-parameters.pkl', 'rb') ).load()
text_vectorizer = CustomUnpickler( open(f'{current_wd}/newsverifier/data/text_vectorizer.pkl', 'rb') ).load()

        
def predict(text):
    
    d = {'text': [text]}

    # create dataframe from user input
    X_df = pd.DataFrame(data=d)

    # preprocess df and return np array
    X_np = preprocess(X_df, text_vectorizer)

    # convert to tensor
    X_tensor = torch.Tensor(X_np)

    # predict
    y_pred = model(X_tensor)
    y_pred_max = torch.max(y_pred, 1)[1]

    if y_pred_max == 1:
        result = "real"
    else:
        result = "fake"
    
    return  result