# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog,QDialog,QSizePolicy,QGridLayout,QMessageBox
from win32api import GetSystemMetrics
from sub_menu import Ui_OtherWindow

class Customer(object):
    def __init__(self,*args):
        args = list(args[0])
        for i in range(len(args)):
            execution = "self.headers_" + str(i) + " = '" + str(args[i]) +"'"
            exec(execution)

class CustomerTableModel(QtCore.QAbstractTableModel):

    def __init__(self,rawHeaders):
        super(CustomerTableModel,self).__init__()
        self.rawHeaders = rawHeaders
        self.headers = list(self.rawHeaders)
        for i in range(len(self.headers)):
            if(len(self.headers[i]) < 5):
                self.headers[i] = "           " + self.headers[i] + "           "
            elif(len(self.headers[i]) <= 10):
                self.headers[i] = "     " + self.headers[i] + "     "
            elif(len(self.rawHeaders[i]) > 10):
                self.headers[i] = "   " + self.headers[i] + "   "
            elif(len(headers[i]) > 20):
                pass
        self.customers  = []
    def rowCount(self,index=QtCore.QModelIndex()):
        return len(self.customers)

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
            for a in range(len(self.headers)+1):
                if(col == a):
                    code = "global WR_var;WR_var = customer.headers_"+str(a)
                    exec(code)
                    return QtCore.QVariant(WR_var)

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
    def setupUi(self, MainWindow, version):

        self.version = version

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1111, 700)
        MainWindow.setMinimumSize(QtCore.QSize(1111, 700))
        MainWindow.setMaximumSize(QtCore.QSize(GetSystemMetrics(0), 700))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setMinimumSize(QtCore.QSize(550, 0))
        self.tableView.setObjectName("tableView")
        self.horizontalLayout.addWidget(self.tableView)

        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)                                                                                                                                                
        self.pushButton.setMinimumSize(QtCore.QSize(507, 28))
        self.pushButton.setMaximumSize(QtCore.QSize(507, 28))
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setMinimumSize(QtCore.QSize(507, 28))
        self.pushButton_2.setMaximumSize(QtCore.QSize(507, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)

        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setMinimumSize(QtCore.QSize(249, 31))
        self.label.setMaximumSize(QtCore.QSize(249, 31))
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)

        self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox.sizePolicy().hasHeightForWidth())
        self.spinBox.setSizePolicy(sizePolicy)
        self.spinBox.setMinimumSize(QtCore.QSize(249, 22))
        self.spinBox.setMaximumSize(QtCore.QSize(249, 22))                              
        self.spinBox.setReadOnly(True)
        self.spinBox.setMaximum(999999)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout_3.addWidget(self.spinBox)

        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setMinimumSize(QtCore.QSize(249, 32))
        self.label_2.setMaximumSize(QtCore.QSize(249, 32))                                     
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)

        self.spinBox_2 = QtWidgets.QSpinBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)        
        sizePolicy.setHeightForWidth(self.spinBox_2.sizePolicy().hasHeightForWidth())
        self.spinBox_2.setSizePolicy(sizePolicy)
        self.spinBox_2.setMinimumSize(QtCore.QSize(249, 22))
        self.spinBox_2.setMaximumSize(QtCore.QSize(249, 22))                                
        self.spinBox_2.setReadOnly(True)
        self.spinBox_2.setMaximum(999999)
        self.spinBox_2.setObjectName("spinBox_2")
        self.horizontalLayout_4.addWidget(self.spinBox_2)

        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setMinimumSize(QtCore.QSize(249, 31))
        self.label_3.setMaximumSize(QtCore.QSize(249, 31))                                     
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_5.addWidget(self.label_3)

        self.spinBox_3 = QtWidgets.QSpinBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)                                        
        sizePolicy.setHeightForWidth(self.spinBox_3.sizePolicy().hasHeightForWidth())
        self.spinBox_3.setSizePolicy(sizePolicy)
        self.spinBox_3.setMinimumSize(QtCore.QSize(249, 22))
        self.spinBox_3.setMaximumSize(QtCore.QSize(249, 22))                                
        self.spinBox_3.setReadOnly(True)
        self.spinBox_3.setMaximum(999999)
        self.spinBox_3.setObjectName("spinBox_3")
        self.horizontalLayout_5.addWidget(self.spinBox_3)

        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setMinimumSize(QtCore.QSize(249, 31))
        self.label_4.setMaximumSize(QtCore.QSize(249, 31))                                     
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_6.addWidget(self.label_4)

        self.spinBox_4 = QtWidgets.QSpinBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)                                
        sizePolicy.setHeightForWidth(self.spinBox_4.sizePolicy().hasHeightForWidth())
        self.spinBox_4.setSizePolicy(sizePolicy)
        self.spinBox_4.setMinimumSize(QtCore.QSize(249, 22))
        self.spinBox_4.setMaximumSize(QtCore.QSize(249, 22))                               
        self.spinBox_4.setReadOnly(True)
        self.spinBox_4.setMaximum(999999)
        self.spinBox_4.setObjectName("spinBox_4")
        self.horizontalLayout_6.addWidget(self.spinBox_4)

        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")

        self.plain = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plain.setMinimumSize(QtCore.QSize(240, 380))
        self.plain.setMaximumSize(QtCore.QSize(240, 380))                                                                    
        self.plain.setObjectName("plain")
        self.horizontalLayout_7.addWidget(self.plain)

        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setMinimumSize(QtCore.QSize(256, 130))
        self.label_5.setMaximumSize(QtCore.QSize(256, 130))
        self.label_5.setObjectName("label_5")
        self.verticalLayout_2.addWidget(self.label_5)

        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setMinimumSize(QtCore.QSize(280, 230))
        self.label_6.setMaximumSize(QtCore.QSize(280, 230))                                                      
        self.label_6.setObjectName("label_6")
        self.verticalLayout_2.addWidget(self.label_6)
        self.horizontalLayout_7.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.gridLayout.addLayout(self.horizontalLayout,0,0,1,1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1100, 26))
        self.menubar.setObjectName("menubar")
        self.menuDosya = QtWidgets.QMenu(self.menubar)
        self.menuDosya.setObjectName("menuDosya")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
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
        self.actionUpdate = QtWidgets.QAction(MainWindow)
        self.actionUpdate.setObjectName("actionUpdate")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuDosya.addAction(self.actionDosya_A)
        self.menuDosya.addAction(self.actionAyarla)
        self.menuDosya.addAction(self.actionKapat)
        self.menuAbout.addAction(self.actionUpdate)
        self.menuAbout.addAction(self.actionAbout)
        self.menubar.addAction(self.menuDosya.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        # Window Title
        MainWindow.setWindowTitle(_translate("MainWindow", "Whatsapp Otomatik Mesaj Programı"))

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
        self.menuAbout.setTitle(_translate("MainWindow", "Hakkında"))
        self.actionDosya_A.setText(_translate("MainWindow", "Dosya Aç..."))
        self.actionDosya_A.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionKapat.setText(_translate("MainWindow", "Kapat"))
        self.actionKapat.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionAyarla.setText(_translate("MainWindow", "Ayarlar"))
        self.actionAyarla.setShortcut(_translate("MainWindow","Ctrl+Shift+A"))
        self.actionUpdate.setText(_translate("MainWindow","Güncelle..."))
        self.actionAbout.setText(_translate("MainWindow","Versiyon\t" + self.version))
import icons

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_()) 

