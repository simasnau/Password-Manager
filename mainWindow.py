from PyQt5 import QtCore, QtWidgets
from PyQt5.Qt import QMainWindow, QTableWidgetItem
import sqlite3, threading
from builtins import str
from simplecrypt import encrypt, decrypt
from base64 import b64encode, b64decode
from addDataWindow import AddDataWindow


class MainWindow(QMainWindow):
    dataLoaded=QtCore.pyqtSignal(object,object,object)

    def __init__(self, username, password):
        super(QMainWindow,self).__init__()
        self.userId=username
        self.key=password
        self.setObjectName("MainWindow")
        self.resize(463*2, 384*2)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.table = QtWidgets.QTableWidget(self.centralwidget)
        self.table.setGeometry(QtCore.QRect(0, 0, 381*2, 351*2))
        self.table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.table.setColumnCount(3)
        self.table.setRowCount(0)
        header_labels=['Site','Username','Password']
        self.table.setHorizontalHeaderLabels(header_labels)

        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.table.setObjectName("tableWidget")
        self.table.horizontalHeader().setVisible(True)
        self.table.verticalHeader().setVisible(True)

        self.addBtn = QtWidgets.QPushButton(self.centralwidget)
        self.addBtn.setGeometry(QtCore.QRect(390*2, 20*2, 56*2, 17*2))
        self.addBtn.setObjectName("addBtn")
        self.addBtn.clicked.connect(self.addData)

        self.delBtn = QtWidgets.QPushButton(self.centralwidget)
        self.delBtn.setGeometry(QtCore.QRect(390*2, 60*2, 56*2, 17*2))
        self.delBtn.setObjectName("delBtn")
        self.delBtn.clicked.connect(self.deleteData)

        self.editBtn = QtWidgets.QPushButton(self.centralwidget)
        self.editBtn.setGeometry(QtCore.QRect(390*2, 100*2, 56*2, 17*2))
        self.editBtn.setObjectName("editBtn")
        self.editBtn.clicked.connect(self.editData)

        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 463*2, 18*2))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.horizontalLayout.addWidget(self.table)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setContentsMargins(-1, 40, -1, 0)
        self.formLayout.setVerticalSpacing(40)
        self.formLayout.setObjectName("formLayout")

        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.addBtn)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.delBtn)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.editBtn)

        self.horizontalLayout.addLayout(self.formLayout)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        loadDataThread=threading.Thread(target=self.loadData)
        self.dataLoaded.connect(self.displayData)
        loadDataThread.start()

    def displayData(self, site,username,password):
        self.table.setRowCount(self.table.rowCount()+1)
        rowIndex=self.table.rowCount()-1
        self.table.setItem(rowIndex,0,QTableWidgetItem(str(site)))
        self.table.setItem(rowIndex,1,QTableWidgetItem(str(username)))
        self.table.setItem(rowIndex,2,QTableWidgetItem(str(password)))

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Main Window"))
        self.addBtn.setText(_translate("MainWindow", "Add"))
        self.delBtn.setText(_translate("MainWindow", "Delete"))
        self.editBtn.setText(_translate("MainWindow", "Edit"))

    def addData(self):
        self.addUI=AddDataWindow()
        self.addUI.show()
        self.addUI.okBut.clicked.connect(lambda: self.okButPressed(False))

    def okButPressed(self, isEdit, oldSite='',oldUsername=''):
        try:
            if not isEdit: self.table.setRowCount(self.table.rowCount()+1)

            self.username=self.addUI.usrBox.text()
            self.site=self.addUI.siteBox.text()
            self.password=self.addUI.passBox.text()
            bPass=b64encode(encrypt(self.key, self.password))

            conn = sqlite3.connect('data')
            cursor=conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS users_data (userId VARCHAR(100), site VARCHAR(100),username VARCHAR(100) , password VARCHAR(255))")
            if isEdit:
                cursor.execute("UPDATE users_data SET site=?, username=?, password=? WHERE userId=? and site=? and username=?",(self.site,self.username,bPass,self.userId,oldSite,oldUsername))
            else:
                cursor.execute("INSERT INTO users_data (userId, site, username, password) VALUES (?,?,?,?)",(self.userId,self.site,self.username,bPass))
            conn.commit()
            conn.close()

            self.addUI.close()


            i=self.table.rowCount()-1

            if isEdit: i=self.table.selectedIndexes()[0].row()

            self.table.setItem(i,0,QTableWidgetItem(str(self.site)))
            self.table.setItem(i,1,QTableWidgetItem(str(self.username)))
            self.table.setItem(i,2,QTableWidgetItem(str(self.password)))


        except Exception as e:
            print(e)

    def loadData(self):
        conn = sqlite3.connect('data')
        cursor=conn.cursor()
        cursor.execute("SELECT site, username, password FROM users_data WHERE userId=?",(self.userId,))
        data=cursor.fetchall()
        for row in data:
            try:
                encPass=b64decode(row[2])
                password=decrypt(self.key, encPass)
                password=password.decode("utf-8")
            except Exception as e:
                print(e)
                password="failed"
            finally: self.dataLoaded.emit(row[0],row[1],password)

    def deleteData(self):
        rows = sorted(set(index.row() for index in self.table.selectedIndexes()),reverse=True)
        if len(rows)>0:
            conn = sqlite3.connect('data')
            cursor=conn.cursor()
            for row in rows:
                delSite=self.table.item(row,0).text()
                delUsrn=self.table.item(row,1).text()
                cursor.execute("DELETE FROM users_data WHERE userId=? and site=? and username=?",(self.userId,delSite,delUsrn))
                self.table.removeRow(row)

            conn.commit()
            conn.close()

    def editData(self):
        try:
            i=self.table.selectedIndexes()[0].row()
            self.addUI=AddDataWindow()
            self.addUI.show()
            self.addUI.siteBox.setText(self.table.item(i, 0).text())
            self.addUI.usrBox.setText(self.table.item(i, 1).text())
            self.addUI.passBox.setText(self.table.item(i, 2).text())
            self.addUI.okBut.clicked.connect(lambda: self.okButPressed(True,self.table.item(i, 0).text(),self.table.item(i, 1).text()))
        except Exception as e:
            print(e)

