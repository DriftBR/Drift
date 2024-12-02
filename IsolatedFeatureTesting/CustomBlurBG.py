import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtGui import QColor

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 400, 200)
        self.setStyleSheet("background-color: #282828;")

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        button = QPushButton()
        button.setFixedSize(80, 30)
        button.setStyleSheet("background-color: #282828; color: white;")

        layout.addStretch()
        layout.addWidget(button)
        layout.addStretch()

        container = QWidget()
        container.setLayout(layout)
        container.setStyleSheet("background-color: transparent;")

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(container)
        self.setLayout(main_layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())


