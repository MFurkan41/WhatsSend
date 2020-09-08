# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog,QDialog,QSizePolicy,QGridLayout,QMessageBox,QProgressBar
from win32api import GetSystemMetrics
from includes.forms.subMenu import Ui_OtherWindow
from includes.funcs.warnmessage import warnMessage
import os,itertools
from appIcons import Icons

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
        self.ScRate = GetSystemMetrics(0)/1920
        self.font = QtGui.QFont("Georgia", 8.8*self.ScRate,weight=-2)

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1111*self.ScRate, 700)
        MainWindow.setMinimumSize(QtCore.QSize(1111*self.ScRate, 700*self.ScRate))
        MainWindow.setMaximumSize(QtCore.QSize(GetSystemMetrics(0), 700*self.ScRate))
        MainWindow.setWindowIcon(QtGui.QIcon(Icons["Standart"]))
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
             
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setMinimumSize(QtCore.QSize(550*self.ScRate, 0))
        self.tableView.setObjectName("tableView")
        self.tableView.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tableView.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
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
        self.pushButton.setMinimumSize(QtCore.QSize(507*self.ScRate, 28*self.ScRate))
        self.pushButton.setMaximumSize(QtCore.QSize(507*self.ScRate, 28*self.ScRate))
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)

        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_4.sizePolicy().hasHeightForWidth())
        self.pushButton_4.setSizePolicy(sizePolicy)                                                                                                                                                
        self.pushButton_4.setMinimumSize(QtCore.QSize(507*self.ScRate, 28*self.ScRate))
        self.pushButton_4.setMaximumSize(QtCore.QSize(507*self.ScRate, 28*self.ScRate))
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout.addWidget(self.pushButton_4)
        
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
        self.spinBox.setMinimumSize(QtCore.QSize(249*self.ScRate, 22*self.ScRate))
        self.spinBox.setMaximumSize(QtCore.QSize(249*self.ScRate, 22*self.ScRate))                              
        self.spinBox.setReadOnly(True)
        self.spinBox.setMaximum(999999)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout_3.addWidget(self.spinBox)

        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setMinimumSize(QtCore.QSize(249*self.ScRate, 32*self.ScRate))
        self.label_2.setMaximumSize(QtCore.QSize(249*self.ScRate, 32*self.ScRate))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        
        self.spinBox_2 = QtWidgets.QSpinBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)        
        sizePolicy.setHeightForWidth(self.spinBox_2.sizePolicy().hasHeightForWidth())
        self.spinBox_2.setSizePolicy(sizePolicy)
        self.spinBox_2.setMinimumSize(QtCore.QSize(249*self.ScRate, 22*self.ScRate))
        self.spinBox_2.setMaximumSize(QtCore.QSize(249*self.ScRate, 22*self.ScRate))                                
        self.spinBox_2.setReadOnly(True)
        self.spinBox_2.setMaximum(999999)
        self.spinBox_2.setObjectName("spinBox_2")
        self.horizontalLayout_4.addWidget(self.spinBox_2)

        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setMinimumSize(QtCore.QSize(249*self.ScRate, 31*self.ScRate))
        self.label_3.setMaximumSize(QtCore.QSize(249*self.ScRate, 31*self.ScRate))                                     
        self.label_3.setObjectName("label_3")
        self.label_3.setFont(self.font)
        self.horizontalLayout_5.addWidget(self.label_3)

        self.spinBox_3 = QtWidgets.QSpinBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)                                        
        sizePolicy.setHeightForWidth(self.spinBox_3.sizePolicy().hasHeightForWidth())
        self.spinBox_3.setSizePolicy(sizePolicy)
        self.spinBox_3.setMinimumSize(QtCore.QSize(249*self.ScRate, 22*self.ScRate))
        self.spinBox_3.setMaximumSize(QtCore.QSize(249*self.ScRate, 22*self.ScRate))                                
        self.spinBox_3.setReadOnly(True)
        self.spinBox_3.setMaximum(999999)
        self.spinBox_3.setObjectName("spinBox_3")
        self.horizontalLayout_5.addWidget(self.spinBox_3)

        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setMinimumSize(QtCore.QSize(249*self.ScRate, 31*self.ScRate))
        self.label_4.setMaximumSize(QtCore.QSize(249*self.ScRate, 31*self.ScRate))                                     
        self.label_4.setObjectName("label_4")
        self.label_4.setFont(self.font)
        self.horizontalLayout_6.addWidget(self.label_4)

        self.spinBox_4 = QtWidgets.QSpinBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)                                
        sizePolicy.setHeightForWidth(self.spinBox_4.sizePolicy().hasHeightForWidth())
        self.spinBox_4.setSizePolicy(sizePolicy)
        self.spinBox_4.setMinimumSize(QtCore.QSize(249*self.ScRate, 22*self.ScRate))
        self.spinBox_4.setMaximumSize(QtCore.QSize(249*self.ScRate, 22*self.ScRate))                               
        self.spinBox_4.setReadOnly(True)
        self.spinBox_4.setMaximum(999999)
        self.spinBox_4.setObjectName("spinBox_4")
        self.horizontalLayout_6.addWidget(self.spinBox_4)

        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")

        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout.addWidget(self.line_3)

        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)                                
        sizePolicy.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy)
        self.pushButton_3.setMinimumSize(QtCore.QSize(30*self.ScRate, 30*self.ScRate))
        self.pushButton_3.setMaximumSize(QtCore.QSize(30*self.ScRate, 30*self.ScRate))
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_2.addWidget(self.pushButton_3)

        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)                                
        sizePolicy.setHeightForWidth(self.pushButton_4.sizePolicy().hasHeightForWidth())
        self.pushButton_4.setSizePolicy(sizePolicy)
        self.pushButton_4.setMinimumSize(QtCore.QSize(30*self.ScRate, 30*self.ScRate))
        self.pushButton_4.setMaximumSize(QtCore.QSize(30*self.ScRate, 30*self.ScRate))
        self.pushButton_4.setObjectName("pushButton_3")
        self.horizontalLayout_2.addWidget(self.pushButton_4)

        self.verticalLayout_7.addLayout(self.horizontalLayout_2)

        self.plain = QtWidgets.QPlainTextEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)                                
        sizePolicy.setHeightForWidth(self.plain.sizePolicy().hasHeightForWidth())
        self.plain.setSizePolicy(sizePolicy)
        self.plain.setMinimumSize(QtCore.QSize(240*self.ScRate, 380*self.ScRate))
        self.plain.setMaximumSize(QtCore.QSize(240*self.ScRate, 380*self.ScRate))                                                                    
        self.plain.setObjectName("plain")
        self.verticalLayout_7.addWidget(self.plain)

        self.horizontalLayout_7.addLayout(self.verticalLayout_7)

        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)                                
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setMinimumSize(QtCore.QSize(256*self.ScRate, 130*self.ScRate))
        self.label_5.setMaximumSize(QtCore.QSize(256*self.ScRate, 130*self.ScRate))
        self.label_5.setObjectName("label_5")
        self.label_5.setFont(self.font)
        self.verticalLayout_2.addWidget(self.label_5)

        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setColumnCount(2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)

        self.tableWidget.setHorizontalHeaderItem(0,QtWidgets.QTableWidgetItem("Dosya Adı"))
        self.tableWidget.setHorizontalHeaderItem(1,QtWidgets.QTableWidgetItem("Mesaj Sırası"))
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tableWidget.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)

        self.tableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableWidget.customContextMenuRequested.connect(self.on_context_menu)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setMinimumSize(QtCore.QSize(220*self.ScRate,280*self.ScRate))
        self.tableWidget.setMaximumSize(QtCore.QSize(220*self.ScRate,280*self.ScRate))
        self.verticalLayout_2.addWidget(self.tableWidget)
        self.create_popup_menu()

        self.horizontalLayout_7.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout_8.addLayout(self.horizontalLayout)
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1100*self.ScRate, 26*self.ScRate))
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
        self.i = 1
        self.list_of_files = [["Mesaj","1"]]
        self.updateTable()

    def create_popup_menu(self, parent=None):
        self.popup_menu = QtWidgets.QMenu()
        self.popup_menu.addAction("Yeni Dosya veya Fotoğraf ekle", self.new_cluster)
        self.popup_menu.addAction("Sil", self.delete_cluster)
        self.popup_menu.addSeparator()
        self.popup_menu.addAction("Yukarı Taşı", self.up_cluster)
        self.popup_menu.addAction("Aşağı Taşı", self.down_cluster)

    def on_context_menu(self, pos):        
        node = self.tableWidget.mapToGlobal(pos)
        self.popup_menu.exec_(self.tableWidget.mapToGlobal(pos))

    def new_cluster(self):
        fileName, _ = QFileDialog.getOpenFileName(self.window, "Yeni Dosya veya Fotoğraf Ekle", os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'), "Tüm Dosyalar (*.*)")
        if(fileName):
            self.i+=1
            self.list_of_files.append([fileName,self.i])
            lall = list(itertools.chain.from_iterable(self.list_of_files))
            for i in lall:
                if(lall.count(i) > 1):
                    warnMessage("Aynı Dosya",QMessageBox.Warning,"Aynı dosyayı iki kere seçemezsiniz.")
                    self.list_of_files.pop()
                    self.i-=1
                    return
            self.updateTable()

    def delete_cluster(self):
        for item in self.tableWidget.selectedIndexes():
            for i in self.list_of_files:
                if(self.tableWidget.item(item.row(),0).text() == "Mesaj"):
                    warnMessage("Uyarı!",QMessageBox.Warning,"'Mesaj' satırını silemezsiniz.")
                elif(self.tableWidget.item(item.row(),0).text() == i[0].split("/")[-1]):
                    self.list_of_files.remove(i)
        self.updateTable()

    def up_cluster(self):
        for item in self.tableWidget.selectedIndexes():
            for i in self.list_of_files:
                if(self.tableWidget.item(item.row(),0).text() == i[0].split("/")[-1]):
                    index = self.list_of_files.index(i)
        try:
            self.list_of_files[index],self.list_of_files[index-1]=self.list_of_files[index-1],self.list_of_files[index]
            self.updateTable()
        except:
            pass

    def down_cluster(self):
        for item in self.tableWidget.selectedIndexes():
            for i in self.list_of_files:
                if(self.tableWidget.item(item.row(),0).text() == i[0].split("/")[-1]):
                    index = self.list_of_files.index(i)
        try:
            self.list_of_files[index],self.list_of_files[index+1]=self.list_of_files[index+1],self.list_of_files[index]
            self.updateTable()
        except:
            pass

    def updateTable(self):
        self.tableWidget.setRowCount(len(self.list_of_files))
        for j in range(len(self.list_of_files)):
            self.list_of_files[j][1] = j+1
        for i in range(len(self.list_of_files)):
            code = "self.tableWidget.setItem("+str(i)+",0,QtWidgets.QTableWidgetItem('"+ self.list_of_files[i][0].split("/")[-1] +"'));" + \
                "self.tableWidget.setItem("+str(i)+",1,QtWidgets.QTableWidgetItem('"+ str(self.list_of_files[i][1]) +"'))"
            exec(code)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        # Window Title
        MainWindow.setWindowTitle(_translate("MainWindow", "Whats Message Sender v"+ self.version))

        self.pushButton.setText(_translate("MainWindow", "Başlat"))
        self.pushButton_4.setText(_translate("MainWindow", "Durdur"))
        self.pushButton_4.setVisible(False)
        
        
        """
        self.pushButton_2.setIcon(QtGui.QIcon(Icons["Preview"]))
        self.pushButton_2.setToolTip(_translate("MainWindow","    Mesajınızın önizlemesine bu <br>butondan bakabilirsiniz."))
        self.pushButton_2.setIconSize(QtCore.QSize(30*self.ScRate, 30*self.ScRate))   
        self.pushButton_2.setStyleSheet('QPushButton{border: 0px solid;}')
        """

        self.pushButton_3.setIcon(QtGui.QIcon(Icons["Report"]))
        self.pushButton_3.setToolTip(_translate("MainWindow","    Atılan mesajların raporunu excel formatında kaydetmek için bu butonu kullanabilirsiniz."))
        self.pushButton_3.setIconSize(QtCore.QSize(30*self.ScRate, 30*self.ScRate))   
        self.pushButton_3.setStyleSheet('QPushButton{border: 0px solid;}')

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
    ui.setupUi(MainWindow,"1.7.1")
    MainWindow.show()
    sys.exit(app.exec_()) 
