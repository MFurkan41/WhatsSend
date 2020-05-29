
class Window(QWidget):
    def __init__(self):
        super().__init__()
 
        self.title = "PyQt5 Tables"
        self.width = 500
        self.height = 400
        self.top = 810 - self.width/2
        self.left = 540 - self.height/2
        
 
 
        self.InitWindow()
 
    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        mainMenu = QMenuBar(self)
        fileMenu = mainMenu.addMenu('Dosya')
        
        exitButton = QAction('Çıkış', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Uygulamadan çık')
        exitButton.triggered.connect(self.close)

        openButton = QAction('Aç...(Excel)', self)
        openButton.setShortcut('Ctrl+O')
        openButton.setStatusTip('Excel dosyası aç')
        openButton.triggered.connect(self.openFileNameDialog)

        fileMenu.addAction(openButton)
        fileMenu.addAction(exitButton)
        #self.creatingTables()
        
        self.show()

    def openFileNameDialog(self):
        global numaralar
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Excel Dosyası Aç", "","Excel Files (*.xlsx)", options=options)
        if fileName:
            excel = GetExcel()
            excel.createList(fileName)
            numaralar = excel.getList()
            self.creatingTables()

    def creatingTables(self):
        global numaralar
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(len(numaralar)+1)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setColumnWidth(1, 200)

        self.tableWidget.setItem(0,0, QTableWidgetItem("İsim"))
        self.tableWidget.setItem(0,1, QTableWidgetItem("Telefon No"))

        for i in range(0,len(numaralar)):
            self.tableWidget.setItem(i+1,0, QTableWidgetItem(numaralar[i][0]))
            self.tableWidget.setItem(i+1,1, QTableWidgetItem(numaralar[i][1]))

        button = QPushButton('Başlat', self)
        button.clicked.connect(self.on_click)
        self.vBoxLayout = QVBoxLayout()
        self.vBoxLayout.addWidget(self.tableWidget)
        self.vBoxLayout.addWidget(button)
        self.setLayout(self.vBoxLayout)

    def on_click(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu') 
        options.add_argument('start-maximized')
        options.add_argument('disable-infobars')
        options.add_argument("--disable-extensions")
        browser = webdriver.Chrome(options=options,executable_path="C:\\Drivers\\chromedriver.exe")
        browser.get("https://web.whatsapp.com")
        save_qr(browser)
        bekle(10)
        #browser.set_window_size(1, 1)

        for i in range(0,len(numaralar)):
            mesaj = "Sayın {}, deneme mesaj.".format(numaralar[i][0])
            url = "https://web.whatsapp.com/send?phone="
            url += str(numaralar[i][1])
            url += "&text="
            url += mesaj
            browser.get(url)
            bekle(3)
            browser.find_element_by_xpath("/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[3]/button").click()