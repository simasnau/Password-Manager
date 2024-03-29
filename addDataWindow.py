from PyQt5 import QtCore, QtWidgets
from PyQt5.Qt import QMainWindow

class AddDataWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow,self).__init__()
        self.setObjectName("Add Data")
        self.setWindowTitle("Add Data")
        self.setEnabled(True)
        self.resize(193*2, 186*2)
        self.setInputMethodHints(QtCore.Qt.ImhNone)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.siteBox = QtWidgets.QLineEdit(self.centralwidget)
        self.siteBox.setGeometry(QtCore.QRect(70*2, 10*2, 100*2, 20*2))
        self.siteBox.setObjectName("siteBox")
        self.usrBox = QtWidgets.QLineEdit(self.centralwidget)
        self.usrBox.setGeometry(QtCore.QRect(70*2, 50*2, 100*2, 20*2))
        self.usrBox.setInputMethodHints(QtCore.Qt.ImhNone)
        self.usrBox.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.usrBox.setObjectName("usrBox")
        self.passBox = QtWidgets.QLineEdit(self.centralwidget)
        self.passBox.setGeometry(QtCore.QRect(70*2, 90*2, 100*2, 20*2))
        self.passBox.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passBox.setObjectName("passBox")
        self.okBut = QtWidgets.QPushButton(self.centralwidget)
        self.okBut.setGeometry(QtCore.QRect(20*2, 130*2, 61*2, 21*2))
        self.okBut.setObjectName("okBut")
        self.cancelBut = QtWidgets.QPushButton(self.centralwidget)
        self.cancelBut.setGeometry(QtCore.QRect(120*2, 130*2, 61*2, 21*2))
        self.cancelBut.setObjectName("cancelBut")
        self.siteLabel = QtWidgets.QLabel(self.centralwidget)
        self.siteLabel.setGeometry(QtCore.QRect(0, 0, 51*2, 41*2))
        self.siteLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.siteLabel.setObjectName("siteLabel")
        self.userLabel = QtWidgets.QLabel(self.centralwidget)
        self.userLabel.setGeometry(QtCore.QRect(0, 40*2, 51*2, 41*2))
        self.userLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.userLabel.setObjectName("userLabel")
        self.passLabel = QtWidgets.QLabel(self.centralwidget)
        self.passLabel.setGeometry(QtCore.QRect(0, 80*2, 51*2,41*2))
        self.passLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.passLabel.setObjectName("passLabel")
        self.setCentralWidget(self.centralwidget)

        self.cancelBut.clicked.connect(self.cancelPressed)

        self.okBut.setText("Ok")
        self.cancelBut.setText("Cancel")
        self.siteLabel.setText("Site:")
        self.userLabel.setText("Username:")
        self.passLabel.setText("Password:")

    def cancelPressed(self):
        self.close()
