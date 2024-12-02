from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTabWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import sys
import random

class TabTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("driftapp.tabbedbrowserfeatureorwhatevertocallthis.test")
        self.setGeometry(100, 100, 800, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        layout.addWidget(self.tabs)
        
        new_tab_button = QPushButton("+ New Tab")
        new_tab_button.clicked.connect(self.add_new_tab)
        layout.addWidget(new_tab_button)
        
        self.add_new_tab()
        
    def add_new_tab(self):
        new_tab = QWidget()
        new_tab_layout = QVBoxLayout(new_tab)
        
        web_view = QWebEngineView()
        random_url = random.choice(["https://www.example.com", "https://www.wikipedia.org", "https://www.python.org"])
        web_view.setUrl(QUrl(random_url))
        new_tab_layout.addWidget(web_view)
        
        self.tabs.addTab(new_tab, "New Tab")
        self.tabs.setCurrentWidget(new_tab)
        
    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
        else:
            sys.exit(1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TabTestWindow()
    window.show()
    sys.exit(app.exec_())
