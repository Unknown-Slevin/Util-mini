import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QTextEdit, QLabel

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('PyQt5 Window')
        self.setGeometry(100, 100, 600, 600)

        # Основной вертикальный layout
        main_layout = QVBoxLayout()

        # Строка 1: Кнопка для вызова функции 1
        self.button1 = QPushButton('Вызвать функцию 1', self)
        self.button1.clicked.connect(self.function1)
        main_layout.addWidget(self.button1)

        # Строка 2: 3 выпадающих списка
        row2_layout = QHBoxLayout()
        self.combo1 = QComboBox(self)
        self.combo1.addItems(['Option 1', 'Option 2', 'Option 3'])
        self.combo2 = QComboBox(self)
        self.combo2.addItems(['Option A', 'Option B', 'Option C'])
        self.combo3 = QComboBox(self)
        self.combo3.addItems(['Item X', 'Item Y', 'Item Z'])
        row2_layout.addWidget(self.combo1)
        row2_layout.addWidget(self.combo2)
        row2_layout.addWidget(self.combo3)
        main_layout.addLayout(row2_layout)

        # Строка 3: Кнопка для вызова функции 2
        self.button2 = QPushButton('Вызвать функцию 2', self)
        self.button2.clicked.connect(self.function2)
        main_layout.addWidget(self.button2)

        # Строка 4: Поле вывода текстовой информации
        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)
        main_layout.addWidget(self.output_text)

        # Строка 5: Кнопка очистки поля вывода
        self.clear_button = QPushButton('Очистить поле вывода', self)
        self.clear_button.clicked.connect(self.clear_output)
        main_layout.addWidget(self.clear_button)

        # Устанавливаем основной layout для окна
        self.setLayout(main_layout)

    def function1(self):
        self.output_text.append('Вызвана функция 1')

    def function2(self):
        self.output_text.append('Вызвана функция 2')

    def clear_output(self):
        self.output_text.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())


