import sys
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLineEdit, QPushButton, QStatusBar, QFrame, QWidget, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings


class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Drift Legacy")
        self.setGeometry(100, 100, 1024, 768)
        self.dark_theme_enabled = True
        self.apply_dark_theme()

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.settings = QWebEngineSettings.globalSettings()
        self.settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)

        main_layout = QVBoxLayout()
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        frame = QFrame(self)
        frame.setFrameShape(QFrame.StyledPanel)
        main_layout.addWidget(frame)
        frame_layout = QVBoxLayout(frame)
        frame_layout.setContentsMargins(0, 0, 0, 0)

        self.move_button = QPushButton("Move Window")
        self.move_button.setCheckable(True)
        self.move_button.toggled.connect(self.toggle_move_window)
        self.move_button.setContextMenuPolicy(Qt.CustomContextMenu)
        self.move_button.customContextMenuRequested.connect(self.handle_move_button_context_menu)
        self.status_bar.addWidget(self.move_button)

        self.version_button = QPushButton("Version")
        self.version_button.clicked.connect(self.show_version)
        self.status_bar.addWidget(self.version_button)

        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Enter URL here")
        self.url_bar.returnPressed.connect(self.navigate)
        self.status_bar.addWidget(self.url_bar)

        self.back_button = QPushButton("<")
        self.back_button.clicked.connect(self.go_back)
        self.status_bar.addWidget(self.back_button)

        self.forward_button = QPushButton(">")
        self.forward_button.clicked.connect(self.go_forward)
        self.status_bar.addWidget(self.forward_button)

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh)
        self.status_bar.addWidget(self.refresh_button)

        self.close_button = QPushButton("")
        self.close_button.setStyleSheet("font-family: 'Segoe MDL2 Assets';")
        self.close_button.clicked.connect(self.close)
        self.status_bar.addPermanentWidget(self.close_button)

        self.maximize_button = QPushButton("")
        self.maximize_button.setStyleSheet("font-family: 'Segoe MDL2 Assets';")
        self.maximize_button.clicked.connect(self.toggle_maximize_restore)
        self.status_bar.addPermanentWidget(self.maximize_button)

        self.minimize_button = QPushButton("")
        self.minimize_button.setStyleSheet("font-family: 'Segoe MDL2 Assets';")
        self.minimize_button.clicked.connect(self.showMinimized)
        self.status_bar.addPermanentWidget(self.minimize_button)

        self.web_view = QWebEngineView()
        frame_layout.addWidget(self.web_view)

        self.load_default_homepage()

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.show()

    def apply_dark_theme(self):
        if self.dark_theme_enabled:
            self.setStyleSheet("""
                background-color: #333;
                color: white;
                QPushButton {
                    background-color: #1e1e1e;
                    color: #ffffff;
                    padding: 6px 12px;
                    border: 2px solid #1a3a5a;
                    border-radius: 0px;
                    font-size: 13px;
                    font-weight: 500;
                    min-width: 80px;
                    margin: 0px 2px;
                }
                QPushButton:hover {
                    background-color: #252525;
                }
                QPushButton:pressed {
                    background-color: #151515;
                }
                QPushButton[font-family='Segoe MDL2 Assets'] {
                    color: white;
                }
                QStatusBar::item {
                    border: none;
                }
                QStatusBar QFrame {
                    background: transparent;
                    border: none;
                }
            """)
        else:
            self.setStyleSheet("""
                background-color: none;
                color: black;
                QPushButton {
                    background-color: #1e1e1e;
                    color: #ffffff;
                    padding: 6px 12px;
                    border: 2px solid #1a3a5a;
                    border-radius: 0px;
                    font-size: 13px;
                    font-weight: 500;
                    min-width: 80px;
                    margin: 0px 2px;
                }
                QPushButton:hover {
                    background-color: #252525;
                }
                QPushButton:pressed {
                    background-color: #151515;
                }
                QPushButton[font-family='Segoe MDL2 Assets'] {
                    color: black;
                }
                QStatusBar::item {
                    border: none;
                }
                QStatusBar QFrame {
                    background: transparent;
                    border: none;
                }
            """)

    def load_default_homepage(self):
        self.web_view.load(QUrl.fromLocalFile("\\nwin.html"))

    def navigate(self):
        url = self.url_bar.text()
        if url:
            if not url.startswith("https://"):
                url = "https://" + url
            self.web_view.load(QUrl(url))

    def go_back(self):
        self.web_view.back()

    def go_forward(self):
        self.web_view.forward()

    def refresh(self):
        self.web_view.reload()

    def toggle_move_window(self, checked):
        if checked:
            self.setCursor(Qt.ClosedHandCursor)
            if not hasattr(self, 'window_drag_position'):
                self.window_drag_position = self.pos() - self.mapFromGlobal(QCursor.pos())
        else:
            self.setCursor(Qt.ArrowCursor)

    def mousePressEvent(self, event):
        if self.move_button.isChecked():
            self.window_drag_position = event.globalPos() - self.pos()

    def mouseMoveEvent(self, event):
        if self.move_button.isChecked():
            self.move(event.globalPos() - self.window_drag_position)

    def handle_move_button_context_menu(self, pos):
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.AltModifier:
            self.dark_theme_enabled = not self.dark_theme_enabled
            self.apply_dark_theme()

    def show_version(self):
        QMessageBox.information(self, "Version", "Drift Legacy 8")

    def keyPressEvent(self, event):
        if event.modifiers() == (Qt.ControlModifier | Qt.AltModifier | Qt.ShiftModifier) and event.key() == Qt.Key_A:
            self.show_popup()

    def show_popup(self):
        QMessageBox.information(self, "", "Version: Drift Legacy 8")

    def toggle_maximize_restore(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()


def main():
    app = QApplication(sys.argv)
    window = BrowserWindow()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
