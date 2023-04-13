import mysql, json
from PyQt6.QtCore import QSize, Qt, QAbstractTableModel
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QDialog, QLineEdit, QDateEdit, QComboBox, \
    QTableWidget, QWidget, QTableWidgetItem, QDialogButtonBox, QVBoxLayout, QMessageBox
from database_connection import create_connection, execute_read_query

with open('config.json', 'r') as file:
    preference = json.load(file)


class WindowApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DBMS of PreUpMoney Project")
        self.setFixedSize(854, 480)
        self.connection = mysql.connector.connect(host=preference['host'], user=preference['user'],
                                                  passwd=preference['password'], database=preference['db_name'])
        self.UIinit()

    def UIinit(self):
        self.table = QTableWidget(self)
        self.table.setFixedSize(650, 440)
        self.table.move(20, 20)

        self.watchbox = QComboBox(self)
        self.watchbox.setFixedSize(140, 50)
        self.watchbox.move(700, 20)
        self.watchbox.addItems(["company", "workers", "clients", "consult", "bank_account", "bank_requs"])
        self.watcharr = [5, 6, 5, 6, 6, 5]
        self.watchfnc()
        self.watchbox.currentIndexChanged.connect(self.watchfnc)

        self.addbtn = QPushButton(self)
        self.addbtn.setText("Добавить")
        self.addbtn.setFixedSize(140, 50)
        self.addbtn.move(700, 120)
        self.addbtn.clicked.connect(self.addfnc)

        self.editbtn = QPushButton(self)
        self.editbtn.setText("Изменить")
        self.editbtn.setFixedSize(140, 50)
        self.editbtn.move(700, 220)
        self.editbtn.clicked.connect(self.editfnc)

        self.deletebtn = QPushButton(self)
        self.deletebtn.setText("Удалить")
        self.deletebtn.setFixedSize(140, 50)
        self.deletebtn.move(700, 320)
        self.deletebtn.clicked.connect(self.deletefnc)

    def watchfnc(self):
        self.data = execute_read_query(self.connection, f"SELECT * FROM {self.watchbox.currentText()}")
        print(self.data)
        if len(self.data) > 0:
            self.table.setRowCount(len(self.data))
            self.table.setColumnCount(len(self.data[len(self.data)-1]))
            for i in range(len(self.data)):
                for j in range(len(self.data[i])):
                    self.table.setItem(i, j, QTableWidgetItem(str(self.data[i][j])))
        else:
            self.table.setRowCount(0)
            self.table.setColumnCount(0)

    def addfnc(self):
        dlg = QDialog(self)
        dlg.setWindowTitle(f"Добавление в {self.watchbox.currentText()}")
        dlg.setFixedSize(300, 120)

        dlglabel = QLabel(dlg)
        dlglabel.setText(f"Введи значения через запятую, не более {self.watcharr[self.watchbox.currentIndex()]}")
        dlglabel.move(10, 10)

        dlgline = QLineEdit(dlg)
        dlgline.setFixedSize(280, 25)
        dlgline.move(10, 40)

        dlgbtn = QPushButton(dlg)
        dlgbtn.setText("Добавить")
        dlgbtn.setFixedSize(70, 30)
        dlgbtn.move(220, 80)
        dlgbtn.clicked.connect(lambda: self.query('add', dlgline.text()))

        dlg.exec()

    def editfnc(self):
        dlg = QDialog(self)
        dlg.setWindowTitle(f"Изменение в {self.watchbox.currentText()}")
        dlg.setFixedSize(300, 120)

        dlglabel = QLabel(dlg)
        dlglabel.setText(f"Введи значения через запятую, не более {self.watcharr[self.watchbox.currentIndex()]}")
        dlglabel.move(10, 10)

        dlgline = QLineEdit(dlg)
        dlgline.setFixedSize(280, 25)
        dlgline.move(10, 40)

        dlgbtn = QPushButton(dlg)
        dlgbtn.setText("Изменить")
        dlgbtn.setFixedSize(70, 30)
        dlgbtn.move(220, 80)
        dlgbtn.clicked.connect(lambda: self.query('edit', dlgline.text()))

        dlg.exec()

    def deletefnc(self):
        dlg = QDialog(self)
        dlg.setWindowTitle(f"Удаление в {self.watchbox.currentText()}")
        dlg.setFixedSize(300, 120)

        dlglabel = QLabel(dlg)
        dlglabel.setText(f"Введи id, максимальный -  {len(self.data)}")
        dlglabel.move(10, 10)

        dlgline = QLineEdit(dlg)
        dlgline.setFixedSize(280, 25)
        dlgline.move(10, 40)

        dlgbtn = QPushButton(dlg)
        dlgbtn.setText("Изменить")
        dlgbtn.setFixedSize(70, 30)
        dlgbtn.move(220, 80)
        dlgbtn.clicked.connect(lambda: self.query('delete', dlgline.text()))

        dlg.exec()

    def query(self, querytype, queryargs):
        match querytype:
            case 'add':
                try:
                    self.data = execute_read_query(self.connection,
                                                   f"INSERT INTO {self.watchbox.currentText()}  VALUES ({queryargs})")
                    self.watchfnc()
                except Exception as e:
                    QMessageBox(self).setText(e).show()
            case 'edit':
                try:
                    self.data = execute_read_query(self.connection,
                                                   f"UPDATE {self.watchbox.currentText()} SET VALUES ({queryargs}) where id_{self.watchbox.currentText()} = {queryargs.split(',')[0]}")
                    self.watchfnc()
                except Exception as e:
                    QMessageBox(self).setText(e).show()
            case 'delete':
                try:
                    self.data = execute_read_query(self.connection, f"DELETE FROM {self.watchbox.currentText()} where id_{self.watchbox.currentText()} = {int(queryargs)}")
                    self.watchfnc()
                except Exception as e:
                    QMessageBox(self).setText(e).show()