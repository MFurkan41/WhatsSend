# -*- coding: utf-8 -*-

from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt, QVariant, QSize, QRect, QMetaObject, QCoreApplication
from PyQt5.QtWidgets import QFileDialog,QDialog,QSizePolicy,QGridLayout,QMessageBox, \
                            QProgressBar, QWidget, QHBoxLayout, QVBoxLayout, QMenuBar, QStatusBar, \
                            QPushButton, QTableView, QAbstractItemView, QLabel, QSpacerItem, QSizePolicy, \
                            QFrame, QSpinBox, QPlainTextEdit, QTabWidget, QTableWidget, QTableWidgetItem, \
                            QMenu, QAction, QMainWindow, QApplication
from win32api import GetSystemMetrics
import os,itertools
from ..appIcons import Icons

from includes import *

class Customer(object):
    def __init__(self,*args):
        args = list(args[0])
        for i in range(len(args)):
            execution = "self.headers_" + str(i) + " = '" + str(args[i]) +"'"
            exec(execution)

class CustomerTableModel(QAbstractTableModel):
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
            elif(len(self.headers[i]) > 20):
                pass
        self.customers  = []
    def rowCount(self,index=QModelIndex()):
        return len(self.customers)

    def addCustomer(self,customer):
        self.beginResetModel()
        self.customers.append(customer)
        self.endResetModel()
 
    def columnCount(self,index=QModelIndex()):
        return len(self.headers)
 
    def data(self,index,role=Qt.DisplayRole):
        col = index.column()
        customer = self.customers[index.row()]

        if role == Qt.DisplayRole:
            for a in range(len(self.headers)+1):
                if(col == a):
                    code = "global WR_var;WR_var = customer.headers_"+str(a)
                    exec(code)
                    return QVariant(WR_var)

            return QVariant()
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignCenter

    def headerData(self,section,orientation,role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return QVariant()
 
        if orientation == Qt.Horizontal:
            return QVariant(self.headers[section])
        return QVariant(int(section + 1))

class Ui_MainWindow(object):
    def setupUi(self, MainWindow, version):
        self.version = version
        self.ScRate = GetSystemMetrics(0)/1920
        self.font = QFont("Georgia", 8.8*self.ScRate,weight=-2)

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1126*self.ScRate, 700)
        MainWindow.setMinimumSize(QSize(1126*self.ScRate, 500*self.ScRate))
        MainWindow.setMaximumSize(QSize(GetSystemMetrics(0), 900*self.ScRate))
        MainWindow.setWindowIcon(QIcon(Icons["Standart"]))

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
             
        self.horizontalLayout_8 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")                                                 
        self.tableView = QTableView(self.centralwidget)
        self.tableView.setMinimumSize(QSize(550*self.ScRate, 0))
        self.tableView.setObjectName("tableView")
        self.verticalLayout_4.addWidget(self.tableView)
        self.tableView.setAcceptDrops(True)
        self.tableView.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tableView.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_9.addWidget(self.label_6)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem)
        self.pushButton_8 = QPushButton(self.centralwidget)
        self.pushButton_8.setObjectName("pushButton_8")
        self.horizontalLayout_9.addWidget(self.pushButton_8)
        self.pushButton_9 = QPushButton(self.centralwidget)
        self.pushButton_9.setObjectName("pushButton_9")
        self.horizontalLayout_9.addWidget(self.pushButton_9)
        self.verticalLayout_4.addLayout(self.horizontalLayout_9)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.line = QFrame(self.centralwidget)
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        self.pushButton = QPushButton(self.centralwidget)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)                                                                                                                                                
        self.pushButton.setMinimumSize(QSize(507*self.ScRate, 28*self.ScRate))
        self.pushButton.setMaximumSize(QSize(507*self.ScRate, 28*self.ScRate))
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)

        self.pushButton_4 = QPushButton(self.centralwidget)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_4.sizePolicy().hasHeightForWidth())
        self.pushButton_4.setSizePolicy(sizePolicy)
        self.pushButton_4.setMinimumSize(QSize(507*self.ScRate, 28*self.ScRate))
        self.pushButton_4.setMaximumSize(QSize(507*self.ScRate, 28*self.ScRate))
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout.addWidget(self.pushButton_4)
        
        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName("label")
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QSize(100*self.ScRate,25*self.ScRate))
        self.label.setMaximumSize(QSize(100*self.ScRate,25*self.ScRate))
        self.label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.horizontalLayout_3.addWidget(self.label)

        self.bar = QProgressBar(self.centralwidget)
        self.bar.setObjectName("bar")
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bar.sizePolicy().hasHeightForWidth())
        self.bar.setSizePolicy(sizePolicy)
        self.bar.setMinimumSize(QSize(430*self.ScRate,25*self.ScRate))
        self.bar.setMaximumSize(QSize(430*self.ScRate,25*self.ScRate))
        #self.bar.setValue(50)
        self.bar.setTextVisible(False)
        self.bar.setStyleSheet("QProgressBar {margin-right: 60px;}")
        self.bar.setAlignment(Qt.AlignLeft | Qt.AlignHCenter) 
        self.horizontalLayout_3.addWidget(self.bar)
        

        #self.horizontalLayout_3.addStretch()
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        
        """
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
        """

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setMinimumSize(QSize(249*self.ScRate, 31*self.ScRate))
        self.label_4.setMaximumSize(QSize(249*self.ScRate, 31*self.ScRate))                                     
        self.label_4.setObjectName("label_4")
        self.label_4.setFont(self.font)
        self.horizontalLayout_6.addWidget(self.label_4)

        self.spinBox_4 = QSpinBox(self.centralwidget)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)                                
        sizePolicy.setHeightForWidth(self.spinBox_4.sizePolicy().hasHeightForWidth())
        self.spinBox_4.setSizePolicy(sizePolicy)
        self.spinBox_4.setMinimumSize(QSize(249*self.ScRate, 22*self.ScRate))
        self.spinBox_4.setMaximumSize(QSize(249*self.ScRate, 22*self.ScRate))                               
        self.spinBox_4.setReadOnly(True)
        self.spinBox_4.setMaximum(999999)
        self.spinBox_4.setObjectName("spinBox_4")
        self.horizontalLayout_6.addWidget(self.spinBox_4)

        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")

        self.line_3 = QFrame(self.centralwidget)
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout.addWidget(self.line_3)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.pushButton_2 = QPushButton(self.centralwidget)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)                                
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        self.pushButton_2.setMinimumSize(QSize(30*self.ScRate, 30*self.ScRate))
        self.pushButton_2.setMaximumSize(QSize(30*self.ScRate, 30*self.ScRate))
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)

        self.pushButton_3 = QPushButton(self.centralwidget)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)                                
        sizePolicy.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy)
        self.pushButton_3.setMinimumSize(QSize(30*self.ScRate, 30*self.ScRate))
        self.pushButton_3.setMaximumSize(QSize(30*self.ScRate, 30*self.ScRate))
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_2.addWidget(self.pushButton_3)

        self.pushButton_7 = QPushButton(self.centralwidget)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)                                
        sizePolicy.setHeightForWidth(self.pushButton_7.sizePolicy().hasHeightForWidth())
        self.pushButton_7.setSizePolicy(sizePolicy)
        self.pushButton_7.setMinimumSize(QSize(30*self.ScRate, 30*self.ScRate))
        self.pushButton_7.setMaximumSize(QSize(30*self.ScRate, 30*self.ScRate))
        self.pushButton_7.setObjectName("pushButton_7")
        self.horizontalLayout_2.addWidget(self.pushButton_7)

        space = QSpacerItem(25, 0, QSizePolicy.Fixed, QSizePolicy.Maximum)
        self.horizontalLayout_2.addItem(space)

        self.pushButton_5 = QPushButton(self.centralwidget)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)                                
        sizePolicy.setHeightForWidth(self.pushButton_5.sizePolicy().hasHeightForWidth())
        self.pushButton_5.setSizePolicy(sizePolicy)
        self.pushButton_5.setMinimumSize(QSize(30*self.ScRate, 30*self.ScRate))
        self.pushButton_5.setMaximumSize(QSize(30*self.ScRate, 30*self.ScRate))
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout_2.addWidget(self.pushButton_5)
        
        self.pushButton_6 = QPushButton(self.centralwidget)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)                                
        sizePolicy.setHeightForWidth(self.pushButton_6.sizePolicy().hasHeightForWidth())
        self.pushButton_6.setSizePolicy(sizePolicy)
        self.pushButton_6.setMinimumSize(QSize(30*self.ScRate, 30*self.ScRate))
        self.pushButton_6.setMaximumSize(QSize(30*self.ScRate, 30*self.ScRate))
        self.pushButton_6.setObjectName("pushButton_6")
        self.horizontalLayout_2.addWidget(self.pushButton_6)

        #self.horizontalLayout_2.addStretch()
        
        self.horizontalLayout_2.setAlignment(Qt.AlignLeft)

        self.verticalLayout_7.addLayout(self.horizontalLayout_2)

        self.tab = QTabWidget()
        self.plain_1 = QPlainTextEdit(self.centralwidget)
        self.plain_1.setPlaceholderText("Mesajınız...")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)                                
        sizePolicy.setHeightForWidth(self.tab.sizePolicy().hasHeightForWidth())
        self.tab.setSizePolicy(sizePolicy)
        self.tab.setMinimumSize(QSize(240*self.ScRate, 380*self.ScRate))
        self.tab.setMaximumSize(QSize(240*self.ScRate, 380*self.ScRate))                                                                    
        self.tab.setObjectName("tab")
        self.tab.addTab(self.plain_1, "Mesaj 1")
        
        self.verticalLayout_7.addWidget(self.tab)

        self.horizontalLayout_7.addLayout(self.verticalLayout_7)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.label_5 = QLabel(self.centralwidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)                                
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setMinimumSize(QSize(256*self.ScRate, 130*self.ScRate))
        self.label_5.setMaximumSize(QSize(256*self.ScRate, 130*self.ScRate))
        self.label_5.setObjectName("label_5")
        self.label_5.setFont(self.font)
        self.verticalLayout_2.addWidget(self.label_5)

        self.tableWidget = QTableWidget(self.centralwidget)
        #self.tableWidget = TableWidgetDragRows(self.centralwidget)
        #self.tableWidget.dropSignal.connect(self.updateTableDrag)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setColumnCount(2)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)

        self.tableWidget.setHorizontalHeaderItem(0,QTableWidgetItem("Dosya Adı"))
        self.tableWidget.setHorizontalHeaderItem(1,QTableWidgetItem("Mesaj Sırası"))
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tableWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableWidget.customContextMenuRequested.connect(self.on_context_menu)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setMinimumSize(QSize(220*self.ScRate,280*self.ScRate))
        self.tableWidget.setMaximumSize(QSize(220*self.ScRate,280*self.ScRate))
        self.verticalLayout_2.addWidget(self.tableWidget)
        self.create_popup_menu()

        self.horizontalLayout_7.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout_8.addLayout(self.horizontalLayout)
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 1100*self.ScRate, 26*self.ScRate))
        self.menubar.setObjectName("menubar")
        self.menuDosya = QMenu(self.menubar)
        self.menuDosya.setObjectName("menuDosya")
        self.menuAbout = QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionDosya_A = QAction(MainWindow)
        self.actionDosya_A.setObjectName("actionDosya_A")
        self.actionKapat = QAction(MainWindow)
        self.actionKapat.setObjectName("actionKapat")
        self.actionAyarla = QAction(MainWindow)
        self.actionAyarla.setObjectName("actionAyarla")
        self.actionUpdate = QAction(MainWindow)
        self.actionUpdate.setObjectName("actionUpdate")
        self.actionFeedBack = QAction(MainWindow)
        self.actionFeedBack.setObjectName("actionFeedBack")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuDosya.addAction(self.actionDosya_A)
        self.menuDosya.addAction(self.actionAyarla)
        self.menuDosya.addAction(self.actionKapat)
        self.menuAbout.addAction(self.actionUpdate)
        self.menuAbout.addAction(self.actionAbout)
        self.menuAbout.addAction(self.actionFeedBack)
        self.menubar.addAction(self.menuDosya.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)
        self.i = 1
        self.list_of_files = [["Mesaj","1"]]
        self.updateTable()

    def create_popup_menu(self, parent=None):
        self.popup_menu = QMenu()
        self.popup_menu.addAction("Yeni Dosya veya Fotoğraf ekle", self.new_cluster)
        self.popup_menu.addAction("Sil", self.delete_cluster)
        self.popup_menu.addSeparator()
        self.popup_menu.addAction("Yukarı Taşı", self.up_cluster)
        self.popup_menu.addAction("Aşağı Taşı", self.down_cluster)

    def on_context_menu(self, pos):        
        node = self.tableWidget.mapToGlobal(pos)
        self.popup_menu.exec_(self.tableWidget.mapToGlobal(pos))

    def new_cluster(self):
        fileName, _ = QFileDialog.getOpenFileNames(self.window, "Yeni Dosya veya Fotoğraf Ekle", os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'), "Tüm Dosyalar (*.*)")
        if(fileName):
            for x in fileName:
                self.i+=1
                self.list_of_files.append([x,self.i])
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
            code = "self.tableWidget.setItem("+str(i)+",0,QTableWidgetItem('"+ self.list_of_files[i][0].split("/")[-1] +"'));" + \
                "self.tableWidget.setItem("+str(i)+",1,QTableWidgetItem('"+ str(self.list_of_files[i][1]) +"'))"
            exec(code)
    
    def updateTableDrag(self,x):
        if x[0] == "s":
            self.itemSource = [x[1],x[2]]
        #elif x[0] == "i":

        elif x[0] == "d":
            c = self.list_of_files[self.itemSource[0]]
            self.list_of_files.pop(self.itemSource[0])
            self.list_of_files.insert(x[1],c)
        self.updateTable()
        print(self.list_of_files)
        self.updateTable()
        """self.dragFiles = []
        for i in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(i,0).text()
            self.dragFiles.append(item)
        print(self.dragFiles)
        for j in range(len(self.dragFiles)-1):
            for x in range(len(self.dragFiles)-1):
                if(self.dragFiles[j] == self.list_of_files[x][0].split("/")[-1]):
                    if(self.list_of_files[x] != self.list_of_files[j]):
                        c = self.list_of_files[x]
                        self.list_of_files.pop(x)
                        self.list_of_files.insert(j, c)
        print(self.dragFiles)
        print(self.list_of_files)"""
        
    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        # Window Title
        MainWindow.setWindowTitle(_translate("MainWindow", "Whats Message Sender v"+ self.version))

        self.pushButton.setText(_translate("MainWindow", "Başlat"))
        self.pushButton_4.setText(_translate("MainWindow", "Durdur"))
        self.pushButton_4.setVisible(False)
        
        self.pushButton_2.setIcon(QIcon(Icons["Preview"]))
        self.pushButton_2.setToolTip(_translate("MainWindow","    Mesajınızın önizlemesine bu <br>butondan bakabilirsiniz."))
        self.pushButton_2.setIconSize(QSize(30*self.ScRate, 30*self.ScRate))   
        self.pushButton_2.setStyleSheet('QPushButton{border: 0px solid;}')
        
        self.pushButton_3.setIcon(QIcon(Icons["Report"]))
        self.pushButton_3.setToolTip(_translate("MainWindow","    Atılan mesajların raporunu excel formatında kaydetmek için bu butonu kullanabilirsiniz."))
        self.pushButton_3.setIconSize(QSize(30*self.ScRate, 30*self.ScRate))   
        self.pushButton_3.setStyleSheet('QPushButton{border: 0px solid;}')

        self.pushButton_7.setIcon(QIcon(Icons["Emoji"]))
        self.pushButton_7.setToolTip(_translate("MainWindow","    Mesajınıza emoji eklemek için bu butonu kullanabilirsiniz, emojiler burada farklı görünsede mesaj atıldığı zaman düzelecektir."))
        self.pushButton_7.setIconSize(QSize(30*self.ScRate, 30*self.ScRate))   
        self.pushButton_7.setStyleSheet('QPushButton{border: 0px solid;}')

        self.pushButton_5.setIcon(QIcon(Icons["Plus"]))
        self.pushButton_5.setToolTip(_translate("MainWindow","    Mesaj kutusu oluşturmak için bu butonu kullanabilirsiniz."))
        self.pushButton_5.setIconSize(QSize(30*self.ScRate, 30*self.ScRate))   
        self.pushButton_5.setStyleSheet('QPushButton{border: 0px solid;}')
        
        self.pushButton_6.setIcon(QIcon(Icons["Minus"]))
        self.pushButton_6.setToolTip(_translate("MainWindow","    Son mesaj kutusunu silmek için bu butonu kullanabilirsiniz."))
        self.pushButton_6.setIconSize(QSize(30*self.ScRate, 30*self.ScRate))   
        self.pushButton_6.setStyleSheet('QPushButton{border: 0px solid;}')

        self.pushButton_8.setText(_translate("MainWindow", "Tabloyu Temizle"))

        self.label.setText(_translate("MainWindow", "0/0 - 0%"))
        self.bar.setValue(0)
        self.label_4.setText(_translate("MainWindow", "Kalan Mesaj Hakkınız :"))
        self.label_5.setText(_translate("MainWindow", "  MESAJINIZI YAZARKEN\n"
"  BUNA DİKKAT EDİNİZ.\n"
"\n"
"Eğer mesajın attığınız kişiye özel\n"
" olması için isim kullanmak\n"
" istiyorsanız, mesajınızda isim\n"
" olmasını istediğiniz yere {}\n"
" işaretlerini koyunuz."))
        """
                self.label_5.setText(_translate("MainWindow", "  MESAJINIZI YAZARKEN\n"
        "  BUNA DİKKAT EDİNİZ.\n"
        "\n"
        "Eğer mesajın attığınız kişiye özel\n"
        " olması için kolon değeri kullanmak\n"
        " istiyorsanız, mesajınızda \n"
        "kullanmak istediğiniz değerleri içeren kolonu;\n"
        " {kolon sıra numarası} Örn. {1}, {2}, {3}\n"
        " şeklinde koyabilirsiniz."))
        """
        self.label_6.setText(_translate("MainWindow", "Yukarıdaki alana dosyanızı sürükleyip\n"
                                                "bırakarak da dosyanızı açabilirsiniz."))
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
        self.actionFeedBack.setText(_translate("MainWindow","Geri Bildirim..."))
import icons

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_()) 

