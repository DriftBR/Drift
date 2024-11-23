from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTabWidget, QMessageBox, QMenuBar, QMenu, QAction, QFileDialog, QLabel, QDialog, QDockWidget, QListWidget, QToolButton, QActionGroup, QComboBox
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtCore import QUrl, Qt, QTimer, QPoint, QObject, QEvent, QPropertyAnimation, QAbstractAnimation
from PyQt5.QtGui import QIcon, QPixmap, QKeySequence, QFont, QCursor
from PyQt5.QtPrintSupport import QPrintDialog
import sys
import os
import time

button_style = """
    QPushButton {
        background-color: #2d2d2d;
        color: #ffffff;
        border-radius: 5px;
        border: 1px solid #404040;
        font-size: 12px;
        min-width: 80px;
        min-height: 20px;
        padding: 5px 0px;
    }
    QPushButton:hover {
        background-color: #404040;
    }
    QPushButton:pressed {
        background-color: #1a1a1a;
    }
    QPushButton:checked {
        background-color: #404040;
        border: 2px solid #606060;
    }
    QMessageBox QPushButton {
        background-color: #2d2d2d;
        color: #ffffff;
        border-radius: 5px;
        border: 1px solid #404040;
        font-size: 12px;
        min-width: 80px;
        min-height: 20px;
        padding: 5px 0px;
    }
    QMessageBox QPushButton:hover {
        background-color: #404040;
    }
    QMessageBox QPushButton:pressed {
        background-color: #1a1a1a;
    }
    QToolButton {
        background-color: #2d2d2d;
        color: #ffffff;
        border-radius: 5px;
        border: 1px solid #404040;
        font-size: 12px;
        min-width: 80px;
        min-height: 20px;
        padding: 5px 0px;
    }
    QToolButton:hover {
        background-color: #404040;
    }
    QToolButton:pressed {
        background-color: #1a1a1a;
    }
    QToolButton:checked {
        background-color: #404040;
        border: 2px solid #606060;
    }
    QComboBox {
        background-color: #2d2d2d;
        color: #ffffff;
        border-radius: 5px;
        border: 1px solid #404040;
        font-size: 12px;
        min-width: 120px;
        min-height: 20px;
        padding: 5px;
    }
    QComboBox:hover {
        background-color: #404040;
    }
    QComboBox:pressed {
        background-color: #1a1a1a;
    }
    QComboBox QAbstractItemView {
        background-color: #2d2d2d;
        color: #ffffff;
        selection-background-color: #404040;
    }
"""

dark_theme = """
    QMainWindow, QDialog {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    QTabWidget::pane {
        border: 1px solid #404040;
        background-color: #1a1a1a;
    }
    QTabBar::tab {
        background-color: #2d2d2d;
        color: #ffffff;
        padding: 8px;
        border: 1px solid #404040;
        border-radius: 5px;
    }
    QTabBar::tab:selected {
        background-color: #404040;
        border: 2px solid #606060;
        border-radius: 10px;
    }
    QTabBar::tab:active {
        background-color: #404040;
        border: 2px solid #606060;
    }
    QLineEdit {
        background-color: #2d2d2d;
        color: #ffffff;
        border: 1px solid #404040;
        border-radius: 5px;
        padding: 7px;
        font-size: 12px;
    }
    QMenuBar {
        background-color: #2d2d2d;
        color: #ffffff;
        border-radius: 5px;
    }
    QMenuBar::item:selected {
        background-color: #404040;
        border-radius: 5px;
    }
    QMenu {
        background-color: #2d2d2d;
        color: #ffffff;
        border-radius: 5px;
    }
    QMenu::item:selected {
        background-color: #404040;
    }
    QMenu::drop-down {
        background-color: #404040;
        border-radius: 5px;
    }
    QLabel {
        color: #ffffff;
        border-radius: 5px;
    }
    QMessageBox {
        background-color: #1a1a1a;
        color: #ffffff;
        border-radius: 5px;
    }
    QListWidget {
        background-color: #2d2d2d;
        color: #ffffff;
        border: 1px solid #404040;
        border-radius: 5px;
    }
    QListWidget::item {
        padding: 5px;
    }
    QListWidget::item:selected {
        background-color: #404040;
    }
    QListWidget::item:hover {
        background-color: #353535;
    }
"""

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About...")
        self.setFixedSize(1000, 600)
        self.click_count = 0
        self.last_click_time = 0
        self.click_timer = QTimer()
        self.click_timer.timeout.connect(self.reset_clicks)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create web view for about.html
        web_view = QWebEngineView()
        about_path = os.path.join(os.path.dirname(__file__), 'Assets', 'about.html')
        web_view.setUrl(QUrl.fromLocalFile(about_path))
        layout.addWidget(web_view)
        
        # Create OK button that overlays the web view
        self.ok_button = QPushButton("OK", self)
        self.ok_button.setFixedSize(80, 20)
        self.ok_button.setStyleSheet(button_style)
        self.ok_button.clicked.connect(self.accept)
        self.ok_button.mouseReleaseEvent = self.handle_mouse_release
        
        # Position button in bottom right corner
        self.ok_button.move(self.width() - self.ok_button.width() - 11, 
                      self.height() - self.ok_button.height() - 3)
        
        # Ensure button stays in position when dialog is resized
        self.resizeEvent = lambda e: self.ok_button.move(
            self.width() - self.ok_button.width() - 11,
            self.height() - self.ok_button.height() - 3
        )

    def handle_mouse_release(self, event):
        if event.button() == Qt.RightButton and event.modifiers() == Qt.AltModifier:
            if self.parent().school_mode:
                current_time = time.time()
                if self.click_count == 0:
                    self.click_timer.start(5000)  # 5 second timer
                
                self.click_count += 1
                self.last_click_time = current_time
                
                if self.click_count >= 5:
                    self.click_timer.stop()
                    self.click_count = 0
                    self.unblockedorsomething()
            event.accept()
        else:
            super(QPushButton, self.ok_button).mouseReleaseEvent(event)

    def reset_clicks(self):
        if self.click_count > 0 and self.click_count < 5:
            self.click_count = 0
            self.parent().school_mode_action.setChecked(False)
            self.parent().toggle_school_mode()
        self.click_timer.stop()

    def unblockedorsomething(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Secret...")
        dialog.setFixedSize(300, 150)
        dialog.setStyleSheet(dark_theme)
        
        layout = QVBoxLayout()
        
        list_widget = QListWidget()
        list_widget.addItem("Someday... coming soon...")
        layout.addWidget(list_widget)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        ok_btn = QPushButton("OK")
        ok_btn.setStyleSheet(button_style)
        ok_btn.clicked.connect(dialog.accept)
        button_layout.addWidget(ok_btn)
        
        layout.addStretch()
        layout.addLayout(button_layout)
        
        dialog.setLayout(layout)
        dialog.exec_()

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
        nwin_path = os.path.join(os.path.dirname(__file__), 'Assets', 'nwin.html')
        self.web_view.setUrl(QUrl.fromLocalFile(nwin_path))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drift Beta 4")
        self.setGeometry(100, 100, 1024, 768)
        self.school_mode = False
        icon_path = os.path.join(os.path.dirname(__file__), 'icon.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Set window to front when loaded
        self.activateWindow()
        self.raise_()
        
        menubar = self.menuBar()
        
        file_menu = menubar.addMenu('File')
        
        open_action = QAction('Open', self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        print_action = QAction('Print', self)
        print_action.triggered.connect(self.print_page)
        file_menu.addAction(print_action)
        
        file_menu.addSeparator()
        
        quit_action = QAction('Quit', self)
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)
        
        special_menu = menubar.addMenu('Special')
        self.school_mode_action = QAction('Education Mode', self)
        self.school_mode_action.setCheckable(True)
        self.school_mode_action.triggered.connect(self.toggle_school_mode)
        special_menu.addAction(self.school_mode_action)
        
        help_menu = menubar.addMenu('Help')
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

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
        
        # Add keyboard shortcuts
        new_tab_shortcut = QAction('New Tab', self)
        new_tab_shortcut.setShortcut(QKeySequence("Ctrl+T"))
        new_tab_shortcut.triggered.connect(self.new_tab_shortcut_triggered)
        self.addAction(new_tab_shortcut)
        
        close_tab_shortcut = QAction('Close Tab', self)
        close_tab_shortcut.setShortcut(QKeySequence("Ctrl+W"))
        close_tab_shortcut.triggered.connect(lambda: self.close_tab(self.tabs.currentIndex()))
        self.addAction(close_tab_shortcut)
        
        # Add middle-click handling
        self.tabs.tabBar().setMouseTracking(True)
        self.tabs.tabBar().mouseReleaseEvent = self.handle_tab_mouse_release
        
        nav_bar = QWidget()
        nav_layout = QHBoxLayout()
        nav_layout.setContentsMargins(2, 2, 2, 2)
        nav_bar.setLayout(nav_layout)
        
        self.back_btn = QPushButton("<--[Go Back]")
        self.back_btn.setStyleSheet(button_style)
        self.forward_btn = QPushButton("[Forward]-->")
        self.forward_btn.setStyleSheet(button_style)
        self.reload_btn = QPushButton("[Refresh]")
        self.reload_btn.setStyleSheet(button_style)
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Enter URL (doesn't need HTTPS prefix)")
        self.new_tab_btn = QPushButton("+ [New Tab]")
        self.new_tab_btn.setStyleSheet(button_style)
        self.new_tab_btn.clicked.connect(self.add_new_tab)

        # Create features button with dropdown menu
        self.features_btn = QToolButton()
        self.features_btn.setText("IceSocial   ")
        self.features_btn.setPopupMode(QToolButton.MenuButtonPopup)
        self.features_btn.setCheckable(True)
        self.features_btn.clicked.connect(self.toggle_ice_social)
        self.features_btn.setStyleSheet(button_style)
        
        features_menu = QMenu()
        features_menu.addAction("Music Player", lambda: self.handle_feature_selection("Music Player"))
        features_menu.addAction("Baguette", lambda: self.handle_feature_selection("Baguette"))
        self.features_btn.setMenu(features_menu)
        
        nav_layout.addWidget(self.back_btn)
        nav_layout.addWidget(self.forward_btn)
        nav_layout.addWidget(self.reload_btn)
        nav_layout.addWidget(self.new_tab_btn)
        nav_layout.addWidget(self.url_bar)
        nav_layout.addWidget(self.features_btn)
        
        layout.addWidget(self.tabs)
        layout.addWidget(nav_bar)
        
        # Add footer label
        footer_label = QLabel("Drift is a beta! Expect things to not work")
        footer_label.setAlignment(Qt.AlignCenter)
        footer_font = QFont("Segoe UI Semilight", 9)
        footer_font.setItalic(True)
        footer_label.setFont(footer_font)
        footer_label.setStyleSheet("color: #808080;")
        layout.addWidget(footer_label)
        
        self.ice_social_dock = QDockWidget(self)
        self.ice_social_dock.setTitleBarWidget(QWidget())
        self.ice_social_dock.setFixedWidth(220)
        self.ice_social_dock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        
        ice_social_widget = QWidget()
        ice_social_layout = QVBoxLayout(ice_social_widget)
        ice_social_layout.setContentsMargins(0, 0, 0, 0)
        
        self.ice_social_view = QWebEngineView()
        self.ice_social_view.setUrl(QUrl("https://icesocial.net"))
        ice_social_layout.addWidget(self.ice_social_view)
        
        self.ice_social_dock.setWidget(ice_social_widget)
        self.addDockWidget(Qt.RightDockWidgetArea, self.ice_social_dock)
        self.ice_social_dock.hide()
        
        self.add_new_tab()
        
        self.back_btn.clicked.connect(lambda: self.current_tab().web_view.back())
        self.forward_btn.clicked.connect(lambda: self.current_tab().web_view.forward())
        self.reload_btn.clicked.connect(lambda: self.current_tab().web_view.reload())
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        
        app = QApplication.instance()
        app.setStyleSheet(dark_theme + button_style)

    def toggle_ice_social(self):
        if self.features_btn.isChecked():
            self.ice_social_dock.show()
        else:
            self.ice_social_dock.hide()

    def handle_feature_selection(self, text):
        if text == "Music Player":
            music_path = os.path.join(os.path.dirname(__file__), 'Assets', 'SongPlay.html')
            self.add_new_tab(QUrl.fromLocalFile(music_path))
            self.ice_social_dock.hide()
            self.features_btn.setChecked(False)
        elif text == "Baguette":
            baguette_path = os.path.join(os.path.dirname(__file__), 'Assets', 'Baguette.html')
            self.add_new_tab(QUrl.fromLocalFile(baguette_path))
            self.ice_social_dock.hide()
            self.features_btn.setChecked(False)
        
    def handle_tab_mouse_release(self, event):
        if event.button() == Qt.MiddleButton:
            tab_index = self.tabs.tabBar().tabAt(event.pos())
            if tab_index != -1:
                self.close_tab(tab_index)
        super(self.tabs.tabBar().__class__, self.tabs.tabBar()).mouseReleaseEvent(event)
        
    def new_tab_shortcut_triggered(self):
        new_tab = self.add_new_tab()
        self.url_bar.setFocus()
        self.url_bar.selectAll()
        
    def toggle_school_mode(self):
        self.school_mode = self.school_mode_action.isChecked()
        if self.school_mode:
            self.setWindowTitle("Drift Education")
            self.features_btn.hide()
            self.ice_social_dock.hide()
        else:
            self.setWindowTitle("Drift Beta 4")
            self.features_btn.show()
            
    def show_about(self):
        dialog = AboutDialog(self)
        dialog.exec_()
        
    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", 
            "HTML Files (*.html);;All Files (*)")
        if file_name:
            with open(file_name, 'r') as f:
                html = f.read()
            new_tab = self.add_new_tab()
            new_tab.web_view.setHtml(html, QUrl.fromLocalFile(file_name))
            
    def print_page(self):
        printer = QPrintDialog()
        if printer.exec_() == QPrintDialog.Accepted:
            self.current_tab().web_view.page().print(printer.printer())
        
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

    def smooth_scroll(self, direction):
        scroll_value = 200  # Adjust the scroll value for smoother scrolling
        current_scroll = self.current_tab().web_view.page().scrollPosition()
        if direction == 'up':
            target_scroll = QPoint(current_scroll.x(), max(current_scroll.y() - scroll_value, 0))  # Ensure not to scroll below 0
        elif direction == 'down':
            target_scroll = QPoint(current_scroll.x(), current_scroll.y() + scroll_value)
        else:
            return

        animation = QPropertyAnimation(self.current_tab().web_view.page(), b'scrollPosition')
        animation.setDuration(300)  # Adjust the duration for smoother animation
        animation.setStartValue(current_scroll)
        animation.setEndValue(target_scroll)
        animation.start(QAbstractAnimation.DeleteWhenStopped)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('WindowsVista')
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
