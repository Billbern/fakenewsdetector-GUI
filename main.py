import sys
from PyQt5.QtWidgets import QApplication
from newsverifier import MainWindow

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    try:
        window.show()
    except Exception as e:
        print(e)
    sys.exit(app.exec_())