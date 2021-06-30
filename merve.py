import cv2
import numpy as np
from PyQt5.QtGui import QFont
from pyzbar.pyzbar import decode
import sys
import sqlite3
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import *

counter = 0
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 640)
cap.set(4, 480)

class manuelAdd (QWidget):

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setGeometry(300, 300, 300, 300)

        self.textbox1 = QLineEdit(self)
        self.textbox1.move(140, 10)
        self.textbox1.resize(150, 30)

        self.textbox2 = QLineEdit(self)
        self.textbox2.move(140, 60)
        self.textbox2.resize(150, 30)

        self.textbox3 = QLineEdit(self)
        self.textbox3.move(140, 110)
        self.textbox3.resize(150, 30)
        self.textbox1.setPlaceholderText("enter the product name")
        self.textbox2.setPlaceholderText("enter the product price")
        self.textbox3.setPlaceholderText("enter the product barcode")

        self.label_1 = QLabel("product name: ", self)
        self.label_1.move(15, 10)

        self.label_2 = QLabel("product price: ", self)
        self.label_2.move(15, 60)

        self.label_3 = QLabel("product barcode: ", self)
        self.label_3.move(15, 110)

        self.button = QPushButton('ADD', self)
        self.button.clicked.connect(self.on_click)
        self.button.move(200, 250)

        self.button2 = QPushButton('MAIN WINDOW', self)
        self.button2.clicked.connect(self.on_click2)
        self.button2.move(10, 250)

        layout.addWidget(self.label_1)
        layout.addWidget(self.label_2)
        layout.addWidget(self.label_3)
        layout.addWidget(self.textbox1)
        layout.addWidget(self.textbox2)
        layout.addWidget(self.textbox3)
        layout.addWidget(self.button)
        layout.addWidget(self.button2)

        self.show()

    def on_click(self, ):
        textbox1Value = self.textbox1.text()
        textbox2Value = self.textbox2.text()
        textbox3Value = self.textbox3.text()
        if self.textbox1.text() == "" or self.textbox2.text() == "" or self.textbox3.text() == "":
            QMessageBox.question(self, 'Message - CINAR TOPTAN PARAKENDE',
                                 "Essential field missing!")
        else:
            basket = sqlite3.connect('basket.sqlite')
            cbas = basket.cursor()
            cbas.execute("CREATE TABLE IF NOT EXISTS basket(ad TEXT,fiyat INT,barkod TEXT)")
            cbas.execute("SELECT * FROM basket ")
            a = cbas.fetchall()
            l = []
            for i in a:
                print(i[2])
                l.append(i[2])
            if textbox3Value not in l:
                veriler = [(textbox1Value, textbox2Value, textbox3Value)]
                for veri in veriler:
                    cbas.execute("""INSERT INTO basket VALUES
                                        (?,?,?)""", veri)
                    QMessageBox.question(self, 'Message - CINAR TOPTAN PARAKENDE',
                                         "ADDİNG SUCCESSFUL!")
            elif textbox3Value in l:
                QMessageBox.question(self, 'Message - CINAR TOPTAN PARAKENDE',
                                     textbox3Value + " is PRE-REGISTERED")
            basket.commit()
            self.textbox1.setText("")
            self.textbox2.setText("")
            self.textbox3.setText("")

    def on_click2(self, ):
        self.w = App()
        self.w.show()
        self.hide()

class payPanel (QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setGeometry(300, 300, 300, 300)
        self.textbox2 = QLineEdit(self)
        self.textbox2.move(140, 60)
        self.textbox2.resize(150, 30)

        self.textbox3 = QLineEdit(self)
        self.textbox3.move(140, 150)
        self.textbox3.resize(150, 30)

        self.textbox2.setPlaceholderText("Enter Coupon Code")
        self.textbox3.setPlaceholderText("Enter amount of many ")
        basket = sqlite3.connect('basket.sqlite')
        cbas = basket.cursor()
        cbas.execute("CREATE TABLE IF NOT EXISTS basket(ad TEXT,fiyat INT,barkod TEXT)")
        basket = sqlite3.connect('basket.sqlite')
        cbas.execute("SELECT * FROM basket ")
        c = cbas.fetchall()

        self.manyofsepet = 0
        for j in c:
            print(j)
            self.manyofsepet += j[1]
        print(str(self.manyofsepet))
        basket.commit()
        self.y = 0
        if self.manyofsepet < 100:
            self.y = (self.manyofsepet - ((self.manyofsepet * 10) / 100))
        if self.manyofsepet >= 100:
            self.y = (self.manyofsepet / 2)

        self.label_1 = QLabel(self)
        self.label_1.setText("The amount you will pay : " + str(self.manyofsepet) + "$")
        self.label_1.move(15, 10)

        self.label_2 = QLabel("Coupon Code: ", self)
        self.label_2.move(15, 60)

        self.label_3 = QLabel("Amount of many: ", self)
        self.label_3.move(15, 150)
        self.label_4 = QLabel(self)
        self.label_4.setGeometry(170, 200, 170, 30)
        self.label_4.move(140, 105)
        self.label_5 = QLabel(self)
        self.label_5.setGeometry(170, 200, 170, 30)
        self.label_5.move(50, 180)
        self.button4 = QPushButton('apply', self)
        self.button4.move(15, 105)
        self.button4.clicked.connect(self.on_click3)

        self.button = QPushButton('Payment', self)
        self.button.clicked.connect(self.on_click)
        self.button.move(200, 250)

        self.button2 = QPushButton('MAIN WINDOW', self)
        self.button2.clicked.connect(self.on_click2)
        self.button2.move(10, 250)

        layout.addWidget(self.label_1)
        layout.addWidget(self.label_2)
        layout.addWidget(self.label_3)

        layout.addWidget(self.textbox2)
        layout.addWidget(self.textbox3)
        layout.addWidget(self.button)
        layout.addWidget(self.button2)
        self.show()

    def on_click(self, ):
        if self.textbox3.text() == "":
            QMessageBox.question(self, 'Message - CINAR TOPTAN PARAKENDE',
                                 "Essential field missing!")
        else:
            textboxValue3 = int(self.textbox3.text())
            textboxValue2 = self.textbox2.text()
            c = int(self.manyofsepet)
            k = textboxValue3 - c
            if textboxValue2 == "":
                self.label_5.setText("Remainder of money: " + str(k))
            elif textboxValue3 >= self.y and self.y != 0:
                self.label_5.setText("Remainder of money: " + str(textboxValue3 - self.y) + "$")

            else:
                QMessageBox.question(self, 'Message - CINAR TOPTAN PARAKENDE',
                                     "Insufficient balance! You have " + str(k) + "$")

    def on_click2(self, ):
        self.p = App()
        self.p.show()
        self.hide()

    def on_click3(self, ):
        textboxValue = self.textbox2.text()
        if textboxValue == 'BASKET10' and self.manyofsepet <= 100:
            self.label_4.setText("New amount:" + str(self.y) + "$")
        elif textboxValue == 'BASKET50' and self.manyofsepet > 100:
            self.label_4.setText("New amount:" + str(self.y) + "$")
        else:
            self.label_4.setText("Invalid!")


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.label_2 = QLabel(" OPTIONS ", self)
        self.button1 = QPushButton('BASKET', self)
        self.button = QPushButton('ALL PRODUCTS', self)
        self.button2 = QPushButton('EXIT', self)
        self.button3 = QPushButton('ADD TO BASKET', self)
        self.button4 = QPushButton('REMOVE TO BASKET', self)
        self.button5 = QPushButton('PAY', self)
        self.label_6 = QLabel(" COUPON : ", self)
        self.box = QCheckBox("%10", self)
        self.box2 = QCheckBox("%50", self)

        self.textbox = QLineEdit(self)
        self.textbox.move(130, 10)
        self.textbox.resize(190, 30)
        self.textbox.setPlaceholderText("qrCode to remove from basket")
        self.box.move(100, 170)
        self.box.resize(320, 40)
        self.box2.move(200, 170)
        self.box2.resize(320, 40)
        button_group = QButtonGroup(self)
        button_group.addButton(self.box2)
        button_group.addButton(self.box)

        self.title = ' MAİN WİNDOW '
        self.left = 100
        self.top = 100
        self.width = 400
        self.height = 400
        self.initUI()

    def initUI(self):
        self.box.stateChanged.connect(self.clickBox)
        self.box2.stateChanged.connect(self.clickBox)
        self.label_2.setFont(QFont('Garamond', 14))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.label_2.setGeometry(170, 200, 170, 50)
        self.label_2.move(160, 10)
        self.label_6.move(10, 170)
        self.textbox.move(200, 290)

        self.button.move(10, 60)
        self.button.clicked.connect(self.on_click)

        self.button1.move(10, 110)
        self.button1.clicked.connect(self.on_click1)

        self.button2.setGeometry(170, 200, 380, 30)
        self.button2.move(10, 330)
        self.button2.clicked.connect(self.on_click2)

        self.button3.setGeometry(170, 200, 170, 30)
        self.button3.move(10, 230)
        self.button3.clicked.connect(self.on_click3)

        self.button4.setGeometry(170, 200, 170, 30)
        self.button4.move(10, 290)
        self.button4.clicked.connect(self.on_click4)

        self.button5.move(150, 110)
        self.button5.clicked.connect(self.on_click5)

        self.show()

    @pyqtSlot()
    def on_click(self, ):
        vbox = QVBoxLayout(self)
        listWidget = QListWidget()
        vbox.addWidget(listWidget)
        listWidget.setGeometry(500, 300, 1000, 500)
        listWidget.setWindowTitle("ALL PRODUCTS")

        products = sqlite3.connect('products.sqlite')
        cpro = products.cursor()

        cpro.execute("SELECT * FROM products ")
        a = cpro.fetchall()
        manyofall = 0
        for i in a:
            manyofall += i[1]
            print(i)
            listWidget.addItem("name: " + str(i[0]) + "                                              "
                                                      "price: " + str(
                i[1]) + "$" + "                                      "
                              " code: " + str(i[2]))
        listWidget.addItem("total cost :   " + str(manyofall) + "$")
        print(str(manyofall))
        listWidget.show()
        products.commit()

    def on_click1(self, ):
        vbox1 = QVBoxLayout(self)
        listWidget1 = QListWidget()
        vbox1.addWidget(listWidget1)
        listWidget1.setWindowTitle("BASKET")
        listWidget1.setGeometry(500, 300, 700, 500)
        basket = sqlite3.connect('basket.sqlite')
        cbas = basket.cursor()
        cbas.execute("CREATE TABLE IF NOT EXISTS basket(ad TEXT,fiyat INT,barkod TEXT)")
        cbas.execute("SELECT * FROM basket ")
        c = cbas.fetchall()
        manyofsepet = 0
        i = 1
        listWidget1.addItem("  name            " + "     price($)           ")
        for j in c:
            print(j)
            manyofsepet += j[1]
            listWidget1.addItem(str(i) + "-) " + str(j[0]) + "              " + str(j[1]) + "$")
            print("name: " + str(j[0]) + "price:  " + str(j[1]) + "$" + " barkod: " + str(j[2]))
            i += 1
        listWidget1.addItem("basket cost:   " + str(manyofsepet) + "$")

        print(str(manyofsepet))
        listWidget1.show()
        basket.commit()

    def on_click2(self, ):
        basket = sqlite3.connect('basket.sqlite')
        cbas = basket.cursor()
        cbas.execute("CREATE TABLE IF NOT EXISTS basket(ad TEXT,fiyat INT,barkod TEXT)")
        cbas.execute("DELETE FROM basket")
        basket.commit()
        sys.exit()

    def on_click3(self, ):
        self.n = manuelAdd()
        self.n.show()
        self.hide()

    def on_click4(self, ):
        basket = sqlite3.connect('basket.sqlite')
        cbas = basket.cursor()
        cbas.execute("CREATE TABLE IF NOT EXISTS basket(ad TEXT,fiyat INT,barkod TEXT)")
        cbas.execute(("SELECT barkod FROM basket"))
        myDataList8 = (cbas.fetchall())

        textboxValue = self.textbox.text()
        if textboxValue == "":
            QMessageBox.question(self, 'Message - CINAR TOPTAN PARAKENDE',
                                 "Deletion could not be performed.Please try again! ")


        elif textboxValue not in str(myDataList8):
            QMessageBox.question(self, 'Message - CINAR TOPTAN PARAKENDE',
                                 "There is no such product in system")

        else:
            print("aaaa")
            cbas.execute("DELETE  from basket WHERE barkod=?", (textboxValue,))
            QMessageBox.question(self, 'Message - CINAR TOPTAN PARAKENDE',
                                 "DELETE SUCCESSFUL!")
        basket.commit()
        self.textbox.setText("")

    def on_click5(self, ):
        self.t = payPanel()
        self.t.show()
        self.hide()

    def clickBox(self, state):
        if state == Qt.Checked:
            if self.sender() == self.box:
                self.box2.setChecked(False)
                QMessageBox.about(self, "BASKET10", "Hi! if you want to use this coupon we have some condition \n"
                                                    "✓ You have to buy less than 100.0 $ \n"
                                                    "✓You have to write BASKET10 in coupon textfile When you pay for your shopping "
                                                    "and you can learn click apply button to see how much dollar you willpay!\n"
                                                    "                 We wish you good shopping          ")


            elif self.sender() == self.box2:
                self.box.setChecked(False)
                QMessageBox.about(self, "BASKET50", "Hi! if you want to use this coupon we have some condition \n"
                                                    "✓ You have to buy more than 100.0 $ \n"
                                                    "✓You have to write BASKET50 in coupon textfile When you pay for your shopping "
                                                    "and you can learn click apply button to see how much dollar you willpay!\n"
                                                    "                   We wish you good shopping           ")


while True:
    counter = 0
    success, img = cap.read()
    for barcode in decode(img):
        myData = barcode.data.decode('utf-8')
        print("barcode of products : ",myData)
        products = sqlite3.connect('products.sqlite')
        cpro = products.cursor()
        cpro.execute("CREATE TABLE IF NOT EXISTS products(ad TEXT,fiyat INT,barkod TEXT)")
        cpro.execute(("SELECT barkod FROM products"))
        myDataList = (cpro.fetchall())

        if myData in str(myDataList):
            cpro.execute("SELECT ad, fiyat FROM products WHERE barkod=?", (myData,))
            record = cpro.fetchone(),
            myOutput = str(record[0][0] + ", " + str(record[0][1]) + "$")
            myColor = (0, 255, 0)
            basket = sqlite3.connect('basket.sqlite')
            cbas = basket.cursor()
            cbas.execute("CREATE TABLE IF NOT EXISTS basket(ad TEXT,fiyat INT,barkod TEXT)")
            cbas.execute(("SELECT barkod FROM basket"))
            myDataList2 = (cbas.fetchall())
            if myData not in str(myDataList2):
                cbas.execute("INSERT INTO basket VALUES(:ad, :fiyat, :barkod )",
                            {
                                'ad': record[0][0],
                                'fiyat': record[0][1],
                                'barkod': myData,
                            })
                basket.commit()
                products.commit()
        else:
            myOutput = 'undefined'
            myColor = (0, 255, 0)
            class App1(QMainWindow):

                def __init__(self):
                    super().__init__()
                    self.buttonb = QPushButton('MAIN WINDOW', self)
                    self.buttona = QPushButton('ADD', self)
                    self.textbox2 = QLineEdit(self)
                    self.textbox = QLineEdit(self)
                    self.textbox.setPlaceholderText("enter the product name")
                    self.textbox2.setPlaceholderText("enter the product price")
                    self.label_2 = QLabel("product price: ", self)
                    self.label_1 = QLabel("product name: ", self)
                    self.title = 'CINAR TOPTAN PARAKENDE'

                    self.left = 100
                    self.top = 100
                    self.width = 400
                    self.height = 400
                    self.initUI()

                def initUI(self):
                    self.setWindowTitle(self.title)
                    self.setGeometry(self.left, self.top, self.width, self.height)

                    self.label_1.move(10, 10)

                    self.label_2.move(10, 80)

                    self.textbox.move(130, 10)
                    self.textbox.resize(200, 30)

                    self.textbox2.move(130, 80)
                    self.textbox2.resize(200, 30)

                    self.buttona.move(300, 280)
                    self.buttona.clicked.connect(self.on_clicka)

                    self.buttonb.move(10, 280)
                    self.buttonb.clicked.connect(self.on_clickb)

                    self.show()

                @pyqtSlot()
                def on_clicka(self, ):
                    textboxValue = self.textbox.text()
                    textbox2Value = self.textbox2.text()
                    if self.textbox.text() == "":
                        QMessageBox.question(self, 'Message - CINAR TOPTAN PARAKENDE',
                                             "Required fields cannot be left blank, registration failed")
                    else:
                        products = sqlite3.connect('products.sqlite')
                        cpro = products.cursor()
                        cpro.execute("CREATE TABLE IF NOT EXISTS products(ad TEXT,fiyat INT,barkod TEXT)")
                        veriler = [(textboxValue, textbox2Value, myData)]
                        for veri in veriler:
                            cpro.execute("""INSERT INTO products VALUES
                                        (?,?,?)""", veri)
                            QMessageBox.question(self, 'Message - CINAR TOPTAN PARAKENDE',
                                                 "ADDING SUCCESSFUL!")
                            products.commit()
                            self.textbox.setText("")
                            self.textbox2.setText("")

                def on_clickb(self, ):
                    self.w = App()
                    self.w.show()
                    self.hide()


            app1 = QApplication(sys.argv)
            window = App1()
            window.show()
            app1.exec()

        pts = np.array([barcode.polygon], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(img, [pts], True, myColor, 5)
        pts2 = barcode.rect
        cv2.putText(img, myOutput, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                    0.9, myColor, 2)

    cv2.imshow('Result', img)
    cv2.waitKey(1)

    if cv2.waitKey(30) & 0xFF == ord("l"):
        app = QApplication(sys.argv)
        ex = App()
        app.exec()
