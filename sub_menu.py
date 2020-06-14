# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox,QHeaderView
from time import sleep as bekle

class Ui_OtherWindow(QtCore.QObject):
    my_signal = QtCore.pyqtSignal(list)
    my_signal2 = QtCore.pyqtSignal(str)
    def __init__(self,MainWindow, headers, apiKey):
        super(Ui_OtherWindow,self).__init__()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(350, 393)
        MainWindow.setMinimumSize(QtCore.QSize(350, 393))
        MainWindow.setMaximumSize(QtCore.QSize(350, 393))
        MainWindow.setWindowFlags(MainWindow.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)

        self.mainWindow = MainWindow
        self.headers = headers

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_4.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout_4.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.verticalLayout_4)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.treeWidget = QtWidgets.QTreeWidget(self.centralwidget)
        self.treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeWidget.customContextMenuRequested.connect(self.on_context_menu)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy)
        self.treeWidget.setObjectName("treeWidget")
        for i in range(len(self.headers)):
            item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
            item_0.setFlags(item_0.flags() | QtCore.Qt.ItemIsEditable)
        self.horizontalLayout.addWidget(self.treeWidget)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(150, -1, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 2, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 350, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.create_popup_menu()
        self.pushButton.clicked.connect(self.saveBtn)
        self.pushButton_2.clicked.connect(self.cancel)
        self.lineEdit.returnPressed.connect(self.saveBtn)

        if type(apiKey) == list:

            self.lineEdit.setText(apiKey[0])
        else:
            self.lineEdit.setText(apiKey)
        self.retranslateUi(MainWindow)
        self.treeWidget.resizeColumnToContents(0)


        root = self.treeWidget.invisibleRootItem()
        child_count = root.childCount()
        for i in range(child_count):
            item = root.child(i)
            url = item.text(0)
            if url == "İsim" or url == "Telefon No (Örn 9053xx..)":
                item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)

            if url == "Mesaj Durumu":
                item.setHidden(True)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def saveBtn(self):
        self.headers = []
        root = self.treeWidget.invisibleRootItem()
        child_count = root.childCount()
        for i in range(child_count):
            item = root.child(i)
            url = item.text(0)
            self.headers.append(url)

        self.my_signal.emit(self.headers)
        
        try:
            self.text = str(self.lineEdit.text())
            self.my_signal2.emit(self.text)
        except TypeError:
            self.my_signal2.emit("")

        self.mainWindow.close()

    def cancel(self):
        self.mainWindow.close()


    def new_cluster(self):
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_0.setText(0,"Yeni Kolon")
        item_0.setFlags(item_0.flags() | QtCore.Qt.ItemIsEditable)

    def delete_cluster(self):
        root = self.treeWidget.invisibleRootItem()
        for item in self.treeWidget.selectedItems():
            liste = [0,1]
            a = False
            for i in liste:
                if(item.text(0) == self.headers[i]):
                    a = True
                    msg = QMessageBox()
                    msg.setWindowTitle("Uyarı")
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("'" + str(self.headers[i])+ "' kolonunu silemezsiniz.")
                    x = msg.exec_()
            if a == True:
                break
            else:
                (item.parent() or root).removeChild(item)

    def create_popup_menu(self, parent=None):
        self.popup_menu = QtWidgets.QMenu()
        self.popup_menu.addAction("Yeni", self.new_cluster)
        self.popup_menu.addAction("Sil", self.delete_cluster)
    def on_context_menu(self, pos):        
        node = self.treeWidget.mapToGlobal(pos)
        self.popup_menu.exec_(self.treeWidget.mapToGlobal(pos))
        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Ayarlar"))
        self.label.setText(_translate("MainWindow", "Anahtarınız"))
        self.label_2.setText(_translate("MainWindow", "Müşteri Liste Kolonları (Ekleme, Silme)"))
        self.treeWidget.headerItem().setText(0, _translate("MainWindow", "Kolonlar"))
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        for i in range(len(self.headers)):
            self.treeWidget.topLevelItem(i).setText(0, _translate("MainWindow", self.headers[i]))
        self.treeWidget.setSortingEnabled(__sortingEnabled)
        self.pushButton.setText(_translate("MainWindow", "Kaydet"))
        self.pushButton_2.setText(_translate("MainWindow","İptal"))
