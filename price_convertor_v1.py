import threading
import time

from PyQt5 import QtWidgets, uic
from price_converor_gui import Ui_Price_convertor
from PyQt5.QtWidgets import QApplication
import sys


class Inventory(QtWidgets.QMainWindow):

    def __init__(self):
        self.ui = Ui_Price_convertor()
        super().__init__()
        self.ui.setupUi(self)
        self.if_exist_exchange = int()
        self.ui.open_file.clicked.connect(lambda x: self.showDialog())
        self.ui.RUN.clicked.connect(lambda x: self.main_work())

        self.Multilinestring1 = """"""
        self.Multilinestring2 = """"""
        with open("new_file.txt", "w", encoding='utf-8') as file1:
            file1.close()
        with open("new_file2.txt", "w", encoding='utf-8') as file2:
            file2.close()

    def showDialog(self):
        print("iam clicked")
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '*.txt')[0]
        name_index_ = fname.rfind("/")
        self.filename = fname
        self.ui.filename.setText(fname[name_index_ + 1:])

    def indices(self, lst, element):
        result = []
        offset = -1
        while True:
            try:
                offset = lst.index(element, offset + 1)
            except ValueError:
                return result
            result.append(offset)

    def check_float(self, potential_float):
        try:
            float(potential_float)
            return True
        except ValueError:
            return False

    def main_work(self):
        stock1 = self.ui.stock1.toPlainText().split(",")
        stock2 = self.ui.stock2.toPlainText().split(",")
        with open(self.filename, 'r', encoding='utf-8', errors='ignore') as file:
            data = file.readlines()
            # print(len(data))
            cnt = 0

            self.ui.progressBar.setMaximum(len(data))
            if self.check_float(self.ui.Exchange_rate.text()) and self.check_float(self.ui.Exchange_rate_now.text()):
                self.if_exist_exchange = float(self.ui.Exchange_rate_now.text()) / float(self.ui.Exchange_rate.text())
            else:
                self.if_exist_exchange = 1
            for string in data:

                self.update()
                cnt += 1
                # print(cnt)
                self.ui.progressBar.setValue(cnt)
                data_index = self.indices(string, ";")
                # print(string[data_index[-1] - 4: data_index[-1] - 1])

                if string[data_index[-6] - 1] == '"' and string[data_index[-6] - 2] == "5" and string[
                    data_index[-6] - 3] == '"':
                    continue

                else:
                    # print(p_ac_vin + " " * (33-len(p_ac_vin)) + "VW        " + price_1)
                    if string[data_index[4] + 1:data_index[5]] == '"AP"':
                        continue

                    if string[data_index[-1] - 4: data_index[-1] - 1] in stock1:
                        self.Multilinestring1 += self.worker(string, data_index, "4+_VW")
                    if string[data_index[-1] - 4: data_index[-1] - 1] in stock2:
                        self.Multilinestring2 += self.worker(string, data_index, "VWACT")
                    else:
                        # self.Multilinestring3 += string
                        continue
            file.close()
        #

        with open("new_file.txt", "a", encoding='utf-8') as file1:
            file1.write(self.first_line("4+_VW"))
            file1.write(self.Multilinestring1)
            file1.close()
        with open("new_file2.txt", "a", encoding='utf-8') as file2:
            file2.write(self.first_line("VWACT"))
            file2.write(self.Multilinestring2)
            file2.close()


        self.ui.label_3.setText("Обробка завершена")
        self.ui.label_3.setStyleSheet("color: green")

    def worker(self, string, data_index, aaa):
        p_ac_vin = "P     " + aaa + string[1:data_index[0] - 1].replace(" ", "")   # Р + акция + винкод без пробелов
        price_1 = round(float(string[data_index[4] + 1:data_index[5]].replace(",", ".")) * self.if_exist_exchange, 2)
        price_2 = round(float(string[data_index[5] + 1:data_index[6]].replace(",", ".")) * self.if_exist_exchange, 2)

        price_1 = str(price_1).replace(".", "")

        price_2 = str(round((price_2 * float(self.ui.discount.text())), 2)).replace(".", "")
        res = (p_ac_vin + " " * (33 - len(p_ac_vin)) + "VW        " + ("0" * (12 - len(price_2)) + price_2) * 2 + "0" * (
                    12 - len(str(price_1))) + price_1 + "\n")
        return res

    def first_line(self, ac):
        start_day = self.ui.start_date.text()[0:2]
        start_month = self.ui.start_date.text()[3:5]
        start_year = self.ui.start_date.text()[6:]
        end_day = self.ui.start_date.text()[0:2]
        end_month = self.ui.start_date.text()[3:5]
        end_year = self.ui.start_date.text()[6:]
        first_string = "H     " + ac + " " * (30 - len(
            ac)) + ac + f"{(start_year + start_month + start_day) * 2 + (end_year + end_month + end_day) * 2}"
        return first_string + "\n"


def main():
    app = QApplication(sys.argv)
    w = Inventory()
    w.show()
    app.exec_()


if __name__ == '__main__':
    t = threading.Thread(target=main)
    t.start()
