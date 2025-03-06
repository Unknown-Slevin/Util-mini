import sys
import json
import os
import serial.tools.list_ports
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QFileDialog, QComboBox, QLabel, QTextEdit, QHBoxLayout
)

import Modbus_rtu
from Modbus_rtu import create_modbus_rtu_packet

CONFIG_FILE = 'config.json'

from Config import Config
from DataFromEplan import DataFromEplan
from Controller import Controller

from DataForPLC import DataPLC
from DriverModbus import DriverModbus

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_config()  # Загружаем конфигурацию при запуске

    def initUI(self):
        self.setWindowTitle('Util mini')
        self.setGeometry(100, 100, 600, 600)

        layout = QVBoxLayout()

        # Кнопка для выбора файла
        self.file_button = QPushButton('Выбрать файл conf', self)
        self.file_button.clicked.connect(self.choose_file)
        layout.addWidget(self.file_button)

        # Кнопка для выбора файла eplan
        self.file_eplan_button = QPushButton('Выбрать файл eplan', self)
        self.file_eplan_button.clicked.connect(self.choose_file_eplan)
        layout.addWidget(self.file_eplan_button)

        # Выпадающий список "порт"
        self.port_combo = QComboBox(self)
        self.port_combo.addItems(self.get_serial_ports())

        # Выпадающий список "скорость"
        self.baudrate_combo = QComboBox(self)
        self.baudrate_combo.addItems(['9600', '14400', '19200', '38400', '57600', '115200'])

        # Выпадающий список "четность"
        self.parity_combo = QComboBox(self)
        self.parity_combo.addItems(['None', 'Even', 'Odd'])


        # Выпадающий список "ID"
        self.id_combo = QComboBox(self)
        self.id_combo.addItems(["Id " + str(x) for x in range(1, 255)])

        layout_Hbox = QHBoxLayout()
        layout_Hbox.addWidget(self.port_combo)
        layout_Hbox.addWidget(self.baudrate_combo)
        layout_Hbox.addWidget(self.parity_combo)
        layout_Hbox.addWidget(self.id_combo)
        layout.addLayout(layout_Hbox)


        # Кнопка "загрузить"
        self.load_button = QPushButton('Загрузить', self)
        self.load_button.clicked.connect(self.load_function)
        layout.addWidget(self.load_button)

        # Кнопка "выгрузить"
        self.unload_button = QPushButton('Выгрузить', self)
        self.unload_button.clicked.connect(self.unload_function)
        layout.addWidget(self.unload_button)

        # Поле для вывода информации
        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)
        layout.addWidget(self.output_text)

        # Кнопка "Очистить"
        self.clear_button = QPushButton('Очистить', self)
        self.clear_button.clicked.connect(self.clear_function)
        layout.addWidget(self.clear_button)

        self.setLayout(layout)

        self.config = Config()
        self.dataFromEplan = DataFromEplan()
        self.controller = Controller(self.config)
        self.dataPLC = DataPLC()

        # тут вызывать функцию конфиг
        # config = твой клас конфига


    def choose_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "", "All Files (*);;Text Files (*.txt)",
                                                   options=options)
        if file_path:
            self.file_button.setText(file_path)  # Изменяем текст кнопки на путь к файлу
            self.output_text.append(f'Выбранный файл: {file_path}')
            print('выбран файл')

    def choose_file_eplan(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "", "All Files (*);;Text Files (*.txt)",
                                                   options=options)
        if file_path:
            self.file_eplan_button.setText(file_path)  # Изменяем текст кнопки на путь к файлу
            self.output_text.append(f'Выбранный файл: {file_path}')
            print('выбран файл')

    def load_function(self):
        # Здесь разместите код для загрузки

        file_path = self.file_button.text()
        self.config.readExel(file_path)
        self.config.printDictionary()


        self.output_text.append('Загрузка...')
        data = create_modbus_rtu_packet(slave_address=1, function='read', data_area='holding', starting_address=1, quantity_of_data=5)
        self.output_text.append(' '.join([hex(b)[2:].zfill(2).upper() for b in data]))

    def unload_function(self):

        file_path_eplan = self.file_eplan_button.text()
        self.dataFromEplan.readExel(file_path_eplan)
        self.dataFromEplan.print()

        for i in range(1, self.dataFromEplan.name_var_length):
            self.dataPLC.addData(self.controller.getValueAndReg(self.dataFromEplan.getVar(i), self.dataFromEplan.getIO(i)))

        self.dataPLC.setBinDigital()
        self.dataPLC.print()

        port_text = self.port_combo.currentText()
        baudrate_text = self.baudrate_combo.currentText()
        parity_combo_text = self.parity_combo.currentText()[:1]
        id_combo_text = self.id_combo.currentText()
        id_combo_text = id_combo_text.replace("Id ", "")

        print(id_combo_text)
        print(port_text)
        print(baudrate_text)
        print(parity_combo_text)

        self.driverModbus = DriverModbus(int(id_combo_text), port_text, int(baudrate_text), 8, parity_combo_text)
        self.driverModbus.sendArrayDataToPLC(self.dataPLC.getData(), self.dataPLC.getLength())
        self.driverModbus.writeLong(self.controller.getRegBinDigit(), self.dataPLC.getBinDigital())

        print("finish")
        # тут прочитать еплан
        # если все гуд записать в контроллер используя настройки ком порта
        self.output_text.append('Выгрузка...')

    def clear_function(self):
        self.output_text.clear()

    def get_serial_ports(self):
        """Возвращает список доступных последовательных портов."""
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports] or ['Нет доступных портов']

    def open_port(self):
        pass

    def save_config(self):
        """Сохраняет текущие настройки в файл конфигурации."""
        config = {
            'file_path': self.file_button.text(),
            'port': self.port_combo.currentText(),
            'baudrate': self.baudrate_combo.currentText(),
            'parity': self.parity_combo.currentText(),
            'id': self.id_combo.currentText()
        }

        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)

    def load_config(self):
        """Загружает настройки из файла конфигурации."""
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                self.file_button.setText(config.get('file_path', 'Выбрать файл'))
                self.port_combo.setCurrentText(config.get('port', ''))
                self.baudrate_combo.setCurrentText(config.get('baudrate', '9600'))
                self.parity_combo.setCurrentText(config.get('parity', 'None'))
                self.id_combo.setCurrentText(config.get('id', 'ID1'))

    def closeEvent(self, event):
        """Событие закрытия приложения, сохраняет конфигурацию."""
        self.save_config()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())