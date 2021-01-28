from PyQt5 import QtCore, QtWidgets
from PyQt5.Qt import QMainWindow, QApplication
import sqlite3, sys, bcrypt
from mainWindow import MainWindow

class LoginBox(QMainWindow):
    def __init__(self):
        super(QMainWindow,self).__init__()
        self.setObjectName("MainWindow")
        self.setEnabled(True)
        self.resize(266*2, 216*2)
        self.setInputMethodHints(QtCore.Qt.ImhNone)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.usernameBox = QtWidgets.QLineEdit(self.centralwidget)
        self.usernameBox.setGeometry(QtCore.QRect(110*2, 20*2, 100*2, 20*2))
        self.usernameBox.setObjectName("usernameBox")

        self.passwBox = QtWidgets.QLineEdit(self.centralwidget)
        self.passwBox.setGeometry(QtCore.QRect(110*2, 60*2, 100*2, 20*2))
        self.passwBox.setInputMethodHints(QtCore.Qt.ImhHiddenText|QtCore.Qt.ImhNoAutoUppercase|QtCore.Qt.ImhNoPredictiveText|QtCore.Qt.ImhSensitiveData)
        self.passwBox.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwBox.setObjectName("passwBox")

        self.loginBut = QtWidgets.QPushButton(self.centralwidget)
        self.loginBut.setGeometry(QtCore.QRect(40*2, 136*2, 61*2, 21*2))
        self.loginBut.setObjectName("loginBut")
        self.loginBut.clicked.connect(self.loginButClicked)


        self.createAccBut = QtWidgets.QPushButton(self.centralwidget)
        self.createAccBut.setGeometry(QtCore.QRect(145*2, 136*2, 61*2, 21*2))
        self.createAccBut.setObjectName("createAccBut")
        self.createAccBut.clicked.connect(self.createAccount)


        self.status = QtWidgets.QLabel(self.centralwidget)
        self.status.setEnabled(True)
        self.status.setGeometry(QtCore.QRect(60*2, 100*2, 141*2, 31*2))
        self.status.setText("")
        self.status.setAlignment(QtCore.Qt.AlignCenter)
        self.status.setWordWrap(True)
        self.status.setObjectName("status")

        self.userLabel = QtWidgets.QLabel(self.centralwidget)
        self.userLabel.setGeometry(QtCore.QRect(30*2, 10*2, 61*2, 41*2))
        self.userLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.userLabel.setObjectName("userLabel")

        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 266*2, 18*2))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)

        self.passwLabel = QtWidgets.QLabel(self.centralwidget)
        self.passwLabel.setGeometry(QtCore.QRect(30*2, 50*2, 61*2, 41*2))
        self.passwLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.passwLabel.setObjectName("passwLabel")

        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Login Window"))
        self.loginBut.setText(_translate("MainWindow", "Login"))
        self.createAccBut.setText(_translate("MainWindow", "Create Account"))
        self.userLabel.setText(_translate("MainWindow", "UserName:"))
        self.passwLabel.setText(_translate("MainWindow", "Password:"))

    def loginButClicked(self):
        username=self.usernameBox.text()
        password=self.passwBox.text()
        conn = sqlite3.connect('data')
        cursor=conn.cursor()
        cursor.execute("CREATE TABLE if not exists users (username VARCHAR(100), password VARCHAR(100))")
        cursor.execute("CREATE TABLE if not exists users_data (userId VARCHAR(100), site VARCHAR(100),username VARCHAR(100) , password VARCHAR(255))")
        cursor.execute("SELECT * FROM users WHERE username=?",(username,))
        conn.commit()
        rows=cursor.fetchall()

        if len(rows)>0:
            row=rows[0]
            hashedPass=row[1]
            if bcrypt.checkpw(password.encode("utf-8"), hashedPass.encode("utf-8")):
                self.mainApp=MainWindow(username, password)
                self.mainApp.show()
                self.close()
            else:
                self.status.setText("Wrong password")

        else:
            self.status.setText("This account does not exist")



    def createAccount(self):
        accExists=False
        self.status.setText("")
        username=self.usernameBox.text()
        bPassword=self.passwBox.text().encode("utf-8")
        hashedPass=bcrypt.hashpw(bPassword,bcrypt.gensalt())
        conn = sqlite3.connect('data')
        cursor=conn.cursor()
        cursor.execute("CREATE TABLE if not exists users (username VARCHAR(100), password VARCHAR(100))")
        cursor.execute("SELECT username FROM users WHERE username=?",(username,))
        conn.commit()

        rows=cursor.fetchall()
        if len(rows)>0:
            accExists=True
            self.status.setText("This account already exists")

        if not accExists:
            cursor.execute("INSERT INTO USERS (username, password) VALUES (?, ?)",(username, hashedPass.decode("utf-8")))
            conn.commit()
            self.status.setText("Account created successfully")


def window():
    app = QApplication(sys.argv)
    loginBox=LoginBox()
    loginBox.show()
    sys.exit(app.exec_())

window()
