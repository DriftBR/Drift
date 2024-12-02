from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTabWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import sys
import os

class BrowserTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        self.web_view = QWebEngineView()
        self.web_view.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.web_view)
        nwin_path = os.path.join(os.path.dirname(__file__), '..', 'Assets', 'nwin.html')
        self.web_view.setUrl(QUrl.fromLocalFile(nwin_path))

class BrowserEngineTest(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("driftapp.browserengine.test")
        self.setGeometry(100, 100, 1024, 768)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.setContentsMargins(0, 0, 0, 0)
        self.tabs.setDocumentMode(True)
        
        nav_bar = QWidget()
        nav_layout = QHBoxLayout()
        nav_layout.setContentsMargins(2, 2, 2, 2)
        nav_bar.setLayout(nav_layout)
        
        self.back_btn = QPushButton("<")
        self.back_btn.setFixedSize(20, 20)
        self.reload_btn = QPushButton("R")
        self.reload_btn.setFixedSize(20, 20)
        self.forward_btn = QPushButton(">")
        self.forward_btn.setFixedSize(20, 20)
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Enter URL (doesn't need HTTPS prefix)")
        self.new_tab_btn = QPushButton("+")
        self.new_tab_btn.setFixedSize(20, 20)
        self.new_tab_btn.clicked.connect(self.add_new_tab)
        
        nav_layout.addWidget(self.back_btn)
        nav_layout.addWidget(self.forward_btn)
        nav_layout.addWidget(self.reload_btn)
        nav_layout.addWidget(self.new_tab_btn)
        nav_layout.addWidget(self.url_bar)
        
        layout.addWidget(self.tabs)
        layout.addWidget(nav_bar)
        
        self.add_new_tab()
        
        self.back_btn.clicked.connect(lambda: self.current_tab().web_view.back())
        self.forward_btn.clicked.connect(lambda: self.current_tab().web_view.forward())
        self.reload_btn.clicked.connect(lambda: self.current_tab().web_view.reload())
        self.url_bar.returnPressed.connect(self.navigate_to_url)

    def add_new_tab(self, url=None):
        new_tab = BrowserTab()
        self.tabs.addTab(new_tab, "New Tab")
        self.tabs.setCurrentWidget(new_tab)
        if url:
            new_tab.web_view.setUrl(QUrl(url))
        new_tab.web_view.urlChanged.connect(lambda url: self.update_url_bar(url))
        new_tab.web_view.titleChanged.connect(lambda title: self.update_tab_title(new_tab, title))
        return new_tab
        
    def current_tab(self):
        return self.tabs.currentWidget()
        
    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
        else:
            sys.exit(1)
        
    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url 
        self.current_tab().web_view.setUrl(QUrl(url))
        self.url_bar.clear()
        
    def update_url_bar(self, url):
        pass
        
    def update_tab_title(self, tab, title):
        index = self.tabs.indexOf(tab)
        if index != -1:
            self.tabs.setTabText(index, title)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BrowserEngineTest()
    window.show()
    sys.exit(app.exec_())
