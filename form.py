# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog,QDialog

class Customer(object):
    def __init__(self,name,number,status):
        self.name = name
        self.number = number
        self.status = status

class CustomerTableModel(QtCore.QAbstractTableModel):

    ROW_BATCH_COUNT = 1000

    def __init__(self):
        super(CustomerTableModel,self).__init__()
        self.headers = ['             İsim             ','  Telefon No (Örn 9053xx..)  ','   Mesaj Durumu   ']
        self.customers  = []
        self.rowsLoaded = CustomerTableModel.ROW_BATCH_COUNT
 
    def rowCount(self,index=QtCore.QModelIndex()):
        if not self.customers:
            return 0
 
        if len(self.customers) <= self.rowsLoaded:
            return len(self.customers)
        else:
            return self.rowsLoaded

    def canFetchMore(self,index=QtCore.QModelIndex()):
        if len(self.customers) > self.rowsLoaded:
            return True
        else:
            return False
 
    def fetchMore(self,index=QtCore.QModelIndex()):
        reminder = len(self.customers) - self.rowsLoaded
        itemsToFetch = min(reminder,CustomerTableModel.ROW_BATCH_COUNT)
        self.beginInsertRows(QtCore.QModelIndex(),self.rowsLoaded,self.rowsLoaded+itemsToFetch-1)
        self.rowsLoaded += itemsToFetch
        self.endInsertRows() 

    def addCustomer(self,customer):
        self.beginResetModel()
        self.customers.append(customer)
        self.endResetModel()
 
    def columnCount(self,index=QtCore.QModelIndex()):
        return len(self.headers)
 
    def data(self,index,role=QtCore.Qt.DisplayRole):
        col = index.column()
        customer = self.customers[index.row()]
        if role == QtCore.Qt.DisplayRole:
            if col == 0:
                return QtCore.QVariant(customer.name)
            elif col == 1:
                return QtCore.QVariant(customer.number)
            elif col == 2:
                return QtCore.QVariant(customer.status)
            return QtCore.QVariant()
        elif role == QtCore.Qt.TextAlignmentRole:
            return QtCore.Qt.AlignCenter

    def headerData(self,section,orientation,role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
 
        if orientation == QtCore.Qt.Horizontal:
            return QtCore.QVariant(self.headers[section])
        return QtCore.QVariant(int(section + 1))

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1100, 700)
        MainWindow.setMinimumSize(QtCore.QSize(1100, 700))
        MainWindow.setMaximumSize(QtCore.QSize(1100, 700))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(30, 20, 1041, 611))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.tableView = QtWidgets.QTableView(self.horizontalLayoutWidget)
        self.tableView.setMinimumSize(QtCore.QSize(550, 0))
        self.tableView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableView.setObjectName("tableView")
        self.horizontalLayout.addWidget(self.tableView)

        self.line = QtWidgets.QFrame(self.horizontalLayoutWidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.line_2 = QtWidgets.QFrame(self.horizontalLayoutWidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.spinBox = QtWidgets.QSpinBox(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox.sizePolicy().hasHeightForWidth())
        self.spinBox.setSizePolicy(sizePolicy)
        self.spinBox.setReadOnly(True)
        self.spinBox.setMaximum(999999)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout_3.addWidget(self.spinBox)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        self.spinBox_2 = QtWidgets.QSpinBox(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox_2.sizePolicy().hasHeightForWidth())
        self.spinBox_2.setSizePolicy(sizePolicy)
        self.spinBox_2.setReadOnly(True)
        self.spinBox_2.setMaximum(999999)
        self.spinBox_2.setObjectName("spinBox_2")
        self.horizontalLayout_4.addWidget(self.spinBox_2)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_3 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_5.addWidget(self.label_3)
        self.spinBox_3 = QtWidgets.QSpinBox(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox_3.sizePolicy().hasHeightForWidth())
        self.spinBox_3.setSizePolicy(sizePolicy)
        self.spinBox_3.setReadOnly(True)
        self.spinBox_3.setMaximum(999999)
        self.spinBox_3.setObjectName("spinBox_3")
        self.horizontalLayout_5.addWidget(self.spinBox_3)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_4 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_6.addWidget(self.label_4)
        self.spinBox_4 = QtWidgets.QSpinBox(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox_4.sizePolicy().hasHeightForWidth())
        self.spinBox_4.setSizePolicy(sizePolicy)
        self.spinBox_4.setReadOnly(True)
        self.spinBox_4.setMaximum(999999)
        self.spinBox_4.setObjectName("spinBox_4")
        self.horizontalLayout_6.addWidget(self.spinBox_4)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")

        self.plain = QtWidgets.QPlainTextEdit(self.horizontalLayoutWidget)
        self.plain.setMinimumSize(QtCore.QSize(0, 380))
        #self.plain.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.plain.setObjectName("plain")
        self.horizontalLayout_7.addWidget(self.plain)

        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_5 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_5.setMinimumSize(QtCore.QSize(250, 0))
        self.label_5.setObjectName("label_5")
        self.verticalLayout_2.addWidget(self.label_5)
        self.label_6 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_2.addWidget(self.label_6)
        self.horizontalLayout_7.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.horizontalLayout.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1100, 26))
        self.menubar.setObjectName("menubar")
        self.menuDosya = QtWidgets.QMenu(self.menubar)
        self.menuDosya.setObjectName("menuDosya")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionDosya_A = QtWidgets.QAction(MainWindow)
        self.actionDosya_A.setObjectName("actionDosya_A")
        self.actionKapat = QtWidgets.QAction(MainWindow)
        self.actionKapat.setObjectName("actionKapat")
        self.actionAyarla = QtWidgets.QAction(MainWindow)
        self.actionAyarla.setObjectName("actionAyarla")
        self.menuDosya.addAction(self.actionDosya_A)
        self.menuDosya.addAction(self.actionAyarla)
        self.menuDosya.addAction(self.actionKapat)
        self.menubar.addAction(self.menuDosya.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Başlat"))
        self.pushButton_2.setText(_translate("MainWindow", "PushButton"))
        self.label.setText(_translate("MainWindow", "Listedeki Toplam Numara Sayısı :"))
        self.label_2.setText(_translate("MainWindow", "Toplam Mesaj Atılan :"))
        self.label_3.setText(_translate("MainWindow", "Atılmamış Mesaj Sayısı :"))
        self.label_4.setText(_translate("MainWindow", "Kalan Mesaj Hakkınız :"))
        self.plain.setPlaceholderText(_translate("MainWindow", "Mesajınız..."))
        self.label_5.setText(_translate("MainWindow", "  MESAJINIZI YAZARKEN\n"
"  BUNA DİKKAT EDİNİZ.\n"
"\n"
"Eğer mesajın attığınız kişiye özel\n"
" olması için isim kullanmak\n"
" istiyorsanız, mesajınızda isim\n"
" olmasını istediğiniz yere {}\n"
" işaretlerini koyunuz."))
        self.label_6.setText(_translate("MainWindow", "<html><body><p style='text-align:center'>QR CODE</p></body></html>"))
        self.menuDosya.setTitle(_translate("MainWindow", "Dosya"))
        self.actionDosya_A.setText(_translate("MainWindow", "Dosya Aç..."))
        self.actionDosya_A.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionKapat.setText(_translate("MainWindow", "Kapat"))
        self.actionKapat.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionAyarla.setText(_translate("MainWindow", "Ayarlar"))
import icons

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_()) 

