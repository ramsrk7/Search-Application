import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Search Application")

        # create input box and label
        input_label = QLabel("What are you looking for?", self)
        input_label.move(50, 50)
        self.input_box = QLineEdit(self)
        self.input_box.move(50, 80)

        # create output label
        self.output_label = QLabel("", self)
        self.output_label.move(50, 120)

        # create button
        button = QPushButton("Submit", self)
        button.move(50, 160)
        button.clicked.connect(self.onClick)

        self.setGeometry(100, 100, 300, 250)
        self.show()

    def onClick(self):
        input_text = self.input_box.text()
        output_text = "Hello " + input_text
        self.output_label.setText(output_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
