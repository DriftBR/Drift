from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTabWidget, QMessageBox, QMenu, QAction, QFileDialog, QTabBar, QComboBox
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage
from PyQt5.QtCore import QUrl, Qt, QTimer, QPoint, QPropertyAnimation, QAbstractAnimation, QSize, QRect, QEvent, QEasingCurve
from PyQt5.QtGui import QIcon, QKeySequence
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
"""

dark_theme = """
    QMainWindow, QDialog {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    QTabWidget::pane {
        border: none;
        background: #1a1a1a;
    }
    QTabBar::tab {
        background-color: #1a1a1a;
        color: #808080;
        padding: 5px 35px 5px 10px;  
        border: none;
        border-radius: 0px;
        height: 30px;
        max-height: 30px;
        min-height: 30px;
    }
    QTabBar::tab:hover:!selected {
        background-color: #252525;
    }
    QTabBar::tab:selected {
        background-color: #1f1f1f;
        border: 1px solid #404040;
        color: #ffffff;
    }
    QTabBar::tab:!selected {
        color: #808080;
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
    QMenu::item {
        background-color: transparent;
        color: #ffffff;
        padding: 8px 25px;
        margin: 2px;
        border-radius: 4px;
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

class CustomWebEnginePage(QWebEnginePage):
    def __init__(self, profile, parent=None):
        super().__init__(profile, parent)
        self.custom_menu = None

    def createStandardContextMenu(self):
        menu = super().createStandardContextMenu()
        self.custom_menu = menu  # Store reference to prevent garbage collection
        
        # Apply custom styling
        menu.setStyleSheet("""
            QMenu {
                background-color: #1a1a1a;
                border: 1px solid #404040;
                border-radius: 10px;
                padding: 5px;
            }
            QMenu::item {
                background-color: transparent;
                color: #ffffff;
                padding: 8px 25px;
                margin: 2px;
                border-radius: 5px;
            }
            QMenu::item:selected {
                background-color: rgba(147, 112, 219, 0.1);
            }
            QMenu::separator {
                height: 1px;
                background-color: #404040;
                margin: 5px 15px;
            }
            QMenu::icon {
                padding-left: 10px;
            }
        """)
        
        return menu

class BrowserTab(QWidget):
    def __init__(self, special_tab=False):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        
        # Create a custom profile with modified user agent
        self.profile = QWebEngineProfile.defaultProfile()
        original_user_agent = self.profile.httpUserAgent()
        modified_user_agent = original_user_agent + " DriftBR"
        self.profile.setHttpUserAgent(modified_user_agent)
        
        # Create web view with custom profile and page
        self.web_view = QWebEngineView()
        custom_page = CustomWebEnginePage(self.profile, self.web_view)
        self.web_view.setPage(custom_page)
        
        self.web_view.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.web_view)
        nwin_path = os.path.join(os.path.dirname(__file__), 'Assets', 'nwin.html')
        self.web_view.setUrl(QUrl.fromLocalFile(nwin_path))
        self.special_tab = special_tab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drift")
        self.setGeometry(100, 100, 1024, 768)
        self.setWindowFlags(Qt.FramelessWindowHint)  
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize_border = 20
        self.dragging = False
        self.resizing = False
        self.resize_edge = None
        self.drag_pos = QPoint()
        self.setMinimumSize(300, 200)
        self.current_search_engine = "Google"  
        
        # Setup animations
        self.slide_animation = QPropertyAnimation(self, b"pos")
        self.slide_animation.setDuration(100)  
        self.slide_animation.setEasingCurve(QEasingCurve.Linear)
        self.slide_animation.finished.connect(self._handle_slide_finished)

        self.zoom_animation = QPropertyAnimation(self, b"geometry")
        self.zoom_animation.setDuration(300)  
        self.zoom_animation.setEasingCurve(QEasingCurve.Linear)
        self.zoom_animation.finished.connect(self._handle_zoom_finished)

        # Store animation states
        self.animation_type = None  
        self.pre_maximize_geometry = None
        
        self.setMouseTracking(True)

        icon_path = os.path.join(os.path.dirname(__file__), 'icon.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        self.activateWindow()
        self.raise_()
        
        self.central_widget = QWidget()
        self.central_widget.setStyleSheet("background-color: #1a1a1a; border: none; border-radius: 10px;")
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Create tab widget
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.setElideMode(Qt.ElideRight)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.setContentsMargins(0, 0, 0, 0)
        self.tabs.setDocumentMode(True)
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                margin-top: -1px; 
                background: transparent;
            }
            QTabBar {
                background: transparent;
            }
            QTabBar::tab {
                color: #808080;
                background-color: transparent;
                border: 1px solid #404040;
                border-radius: 10px;
                padding: 0 10px;
                height: 26px;
                min-height: 26px;
                max-height: 26px;
                margin: 2px;
                margin-bottom: 1px;
            }
            QTabBar::tab:hover:!selected {
                background-color: rgba(64, 64, 64, 0.3);
            }
            QTabBar::tab:selected {
                background-color: #1f1f1f;
                color: #ffffff;
                border: 1px solid #606060;
            }
            QTabBar::close-button {
                image: none;
                width: 16px;
                height: 16px;
                padding: 4px;
                margin-right: 4px;
                border-radius: 10px;
            }
            QTabBar::close-button:hover {
                background: rgba(255, 255, 255, 0.1);
            }
            QTabBar::tab:!selected {
                padding-right: 10px;  
            }
            QTabBar::tab:!selected .close-button {
                width: 0;
                padding: 0;
                margin: 0;
            }
            QTabBar::close-button:!selected {
                image: none;
                width: 0;
                padding: 0;
                margin: 0;
            }
        """)
        self.layout.addWidget(self.tabs)

        # Create window controls for left corner
        left_corner = QWidget()
        left_layout = QHBoxLayout(left_corner)
        left_layout.setContentsMargins(8, 0, 8, 0)
        left_layout.setSpacing(2)
        left_layout.setAlignment(Qt.AlignVCenter)

        # Create a container for window controls
        controls_widget = QWidget()
        controls_layout = QHBoxLayout(controls_widget)
        controls_layout.setContentsMargins(0, 0, 0, 0)
        controls_layout.setSpacing(2)
        
        button_style = """
            QPushButton {
                background-color: transparent;
                border: none;
                color: #ffffff;
                min-width: 14px;
                max-width: 14px;
                min-height: 14px;
                max-height: 14px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 7px;
                margin-right: 2px;
            }
        """
        
        close_btn = QPushButton("")
        close_btn.setStyleSheet(button_style + """
            QPushButton {
                background-color: #FF4141;
            }
            QPushButton:hover {
                background-color: #FF5252;
            }
        """)
        
        minimize_btn = QPushButton("")
        minimize_btn.setStyleSheet(button_style + """
            QPushButton {
                background-color: #FFB900;
            }
            QPushButton:hover {
                background-color: #FFC926;
            }
        """)
        
        self.maximize_btn = QPushButton("")
        self.maximize_btn.setStyleSheet(button_style + """
            QPushButton {
                background-color: #2ECC40;
            }
            QPushButton:hover {
                background-color: #40DB52;
            }
        """)
        
        icon_path = os.path.join(os.path.dirname(__file__), 'icon.ico')
        self.drift_btn = QPushButton()
        if os.path.exists(icon_path):
            self.drift_btn.setIcon(QIcon(icon_path))
            self.drift_btn.setIconSize(QSize(20, 20))
        
        self.drift_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 1px solid #404040;
                color: #ffffff;
                min-width: 24px;
                max-width: 24px;
                min-height: 24px;
                max-height: 24px;
                font-size: 12px;
                font-weight: bold;
                border-radius: 10px;
                margin: 3px;
            }
            QPushButton:hover {
                background-color: rgba(147, 112, 219, 0.1);
                border: 1px solid #606060;
            }
            QPushButton::menu-indicator {
                image: none;
                width: 0;
            }
        """)

        # Create drift menu
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #1a1a1a;
                border: 1px solid #404040;
                border-radius: 10px;
                padding: 5px;
            }
            QMenu::item {
                background-color: transparent;
                color: #ffffff;
                padding: 8px 25px;
                margin: 2px;
                border-radius: 5px;
            }
            QMenu::item:selected {
                background-color: rgba(147, 112, 219, 0.1);
            }
            QMenu::separator {
                height: 1px;
                background-color: #404040;
                margin: 5px 15px;
            }
            QMenu::section {
                padding: 5px 25px;
                color: #9370DB;
                font-weight: bold;
                font-size: 11px;
            }
        """)

        menu.addSection("Drift Menu")

        drift_pad_action = QAction("DriftPad", self)
        drift_pad_action.triggered.connect(self.open_drift_pad)
        menu.addAction(drift_pad_action)
        
        midi_player_action = QAction("MIDI Player", self)
        midi_player_action.triggered.connect(self.open_midi_player)
        menu.addAction(midi_player_action)
        
        open_action = QAction('Open', self)
        open_action.triggered.connect(self.open_file)
        menu.addAction(open_action)

        menu.addSeparator()

        # Add Search Engine submenu
        search_menu = QMenu('Search Engine', self)
        search_menu.setStyleSheet(menu.styleSheet())
        
        search_engines = {
            "Google": lambda: self.set_search_engine("Google"),
            "Yahoo": lambda: self.set_search_engine("Yahoo")
        }
        
        for engine, handler in search_engines.items():
            action = QAction(engine, self)
            action.setCheckable(True)
            action.setChecked(engine == self.current_search_engine)
            action.triggered.connect(handler)
            search_menu.addAction(action)
        
        menu.addMenu(search_menu)
        
        menu.addSeparator()
        
        about_action = QAction('About Drift', self)
        about_action.triggered.connect(self.show_about)
        menu.addAction(about_action)
        
        quit_action = QAction('Quit', self)
        quit_action.triggered.connect(self.close)
        menu.addAction(quit_action)
        
        self.drift_btn.setMenu(menu)
        
        # Add controls to their container
        controls_layout.addWidget(close_btn)
        controls_layout.addWidget(minimize_btn)
        controls_layout.addWidget(self.maximize_btn)

        # Add both containers to main layout with spacing
        left_layout.addWidget(controls_widget)
        spacer = QWidget()
        spacer.setFixedWidth(8)  
        left_layout.addWidget(spacer)
        left_layout.addWidget(self.drift_btn)
        self.tabs.setCornerWidget(left_corner, Qt.TopLeftCorner)

        # Connect button signals
        close_btn.clicked.connect(self.close)
        minimize_btn.clicked.connect(self.showMinimized)
        self.maximize_btn.clicked.connect(self.toggle_maximize)

        # Create new tab button for right corner
        right_corner = QWidget()
        right_layout = QHBoxLayout(right_corner)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)
        
        self.new_tab_btn = QPushButton("+")
        self.new_tab_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: #ffffff;
                min-width: 30px;
                max-width: 30px;
                min-height: 30px;
                max-height: 30px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 0px;
            }
            QPushButton:hover {
                background-color: #404040;
            }
        """)
        self.new_tab_btn.clicked.connect(self.add_new_tab)
        right_layout.addWidget(self.new_tab_btn)
        self.tabs.setCornerWidget(right_corner, Qt.TopRightCorner)

        # Add everything to main layout
        nav_bar = QWidget()
        nav_layout = QHBoxLayout()
        nav_layout.setContentsMargins(2, 2, 2, 2)
        nav_bar.setLayout(nav_layout)
        nav_bar.setStyleSheet("""
            QWidget {
                background-color: #2d2d2d;
                border-bottom-left-radius: 10px;
                border-bottom-right-radius: 10px;
            }
        """)
        
        nav_button_style = """
            QPushButton {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #404040;
                border-radius: 10px;
                font-size: 14px;
                min-width: 30px;
                max-width: 30px;
                min-height: 30px;
                max-height: 30px;
                padding: 0;
                margin: 0;
                line-height: 30px;
            }
            QPushButton:hover {
                background-color: #404040;
            }
            QPushButton:pressed {
                background-color: #1a1a1a;
            }
        """

        input_style = """
            QLineEdit {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #404040;
                border-radius: 10px;
                padding: 5px 10px;
                selection-background-color: #404040;
            }
            QLineEdit:focus {
                border: 1px solid #606060;
            }
            QComboBox {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #404040;
                border-radius: 10px;
                padding: 5px 10px;
                min-width: 100px;
            }
            QComboBox:hover {
                background-color: #404040;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #ffffff;
                width: 0;
                height: 0;
                margin-right: 5px;
            }
        """
        
        self.back_btn = QPushButton("←")
        self.back_btn.setStyleSheet(nav_button_style)
        self.forward_btn = QPushButton("→")
        self.forward_btn.setStyleSheet(nav_button_style)
        self.reload_btn = QPushButton("⟳")
        self.reload_btn.setStyleSheet(nav_button_style)
        
        url_search_container = QWidget()
        url_search_layout = QHBoxLayout()
        url_search_layout.setContentsMargins(0, 0, 0, 0)
        url_search_layout.setSpacing(5)
        url_search_container.setLayout(url_search_layout)
        
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Enter URL (doesn't need HTTPS prefix)")
        self.url_bar.setStyleSheet(input_style)
        
        search_container = QWidget()
        search_layout = QHBoxLayout()
        search_layout.setContentsMargins(0, 0, 0, 0)
        search_layout.setSpacing(2)
        search_container.setLayout(search_layout)
        
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search with Google")
        self.search_bar.setStyleSheet(input_style)
        
        # Set size policies for proper proportions
        url_search_container.setMinimumWidth(int(nav_bar.width() * 0.75))
        search_container.setMinimumWidth(int(nav_bar.width() * 0.25))
        
        # Add widgets to layouts
        search_layout.addWidget(self.search_bar)
        
        url_search_layout.addWidget(self.url_bar, 3)  
        url_search_layout.addWidget(search_container, 1)  
        
        nav_layout.addWidget(self.back_btn)
        nav_layout.addWidget(self.forward_btn)
        nav_layout.addWidget(self.reload_btn)
        nav_layout.addWidget(url_search_container)
        
        self.layout.addWidget(nav_bar)
        
        self.add_new_tab()
        
        self.back_btn.clicked.connect(lambda: self.current_tab().web_view.back())
        self.forward_btn.clicked.connect(lambda: self.current_tab().web_view.forward())
        self.reload_btn.clicked.connect(lambda: self.current_tab().web_view.reload())
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.search_bar.returnPressed.connect(self.perform_search)
        
        new_tab_shortcut = QAction('New Tab', self)
        new_tab_shortcut.setShortcut(QKeySequence("Ctrl+T"))
        new_tab_shortcut.triggered.connect(self.new_tab_shortcut_triggered)
        self.addAction(new_tab_shortcut)
        
        close_tab_shortcut = QAction('Close Tab', self)
        close_tab_shortcut.setShortcut(QKeySequence("Ctrl+W"))
        close_tab_shortcut.triggered.connect(lambda: self.close_tab(self.tabs.currentIndex()))
        self.addAction(close_tab_shortcut)
        
        back_shortcut = QAction('Back', self)
        back_shortcut.setShortcut(QKeySequence("Alt+Left"))
        back_shortcut.triggered.connect(lambda: self.current_tab().web_view.back() if self.current_tab().web_view.history().canGoBack() else None)
        self.addAction(back_shortcut)
        
        forward_shortcut = QAction('Forward', self)
        forward_shortcut.setShortcut(QKeySequence("Alt+Right"))
        forward_shortcut.triggered.connect(lambda: self.current_tab().web_view.forward() if self.current_tab().web_view.history().canGoForward() else None)
        self.addAction(forward_shortcut)
        
        QApplication.instance().installEventFilter(self)
        
        app = QApplication.instance()
        app.setStyleSheet(dark_theme + button_style)
        
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
                border: 1px solid #404040;
                border-radius: 10px;
            }
            * {
                font-family: "Segoe UI", Arial, sans-serif;
            }
            QWidget {
                background-color: transparent;
            }
        """)
        
    def open_drift_pad(self):
        notes_path = os.path.join(os.path.dirname(__file__), 'Assets', 'notesapp.html')
        self.add_new_tab(QUrl.fromLocalFile(notes_path), special_tab=True)

    def open_midi_player(self):
        midi_path = os.path.join(os.path.dirname(__file__), 'Assets', 'midiplayer.html')
        self.add_new_tab(QUrl.fromLocalFile(midi_path), special_tab=True)

    def toggle_maximize(self):
        if self.isMaximized():
            # Start restore animation
            self.zoom_animation.setStartValue(self.geometry())
            self.zoom_animation.setEndValue(self.pre_maximize_geometry)
            self.zoom_animation.setDuration(150)
            self.zoom_animation.setEasingCurve(QEasingCurve.OutQuad)
            self.zoom_animation.start()
        else:
            # Store current geometry before maximizing
            self.pre_maximize_geometry = self.geometry()
            
            # Start maximize animation
            screen = QApplication.primaryScreen().availableGeometry()
            self.zoom_animation.setStartValue(self.geometry())
            self.zoom_animation.setEndValue(screen)
            self.zoom_animation.setDuration(150)
            self.zoom_animation.setEasingCurve(QEasingCurve.OutQuad)
            self.zoom_animation.start()

    def show_about(self):
        about_path = os.path.join(os.path.dirname(__file__), 'Assets', 'about.html')
        self.create_new_tab()
        current_tab = self.tabs.currentWidget()
        current_tab.web_view.setUrl(QUrl.fromLocalFile(about_path))
        
    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", 
            "HTML Files (*.html);;Images (*.png *.jpg *.jpeg, *.gif, *.jfjf, *.bmp);;All Files (*)")
        if file_name:
            with open(file_name, 'r') as f:
                html = f.read()
            new_tab = self.add_new_tab()
            new_tab.web_view.setHtml(html, QUrl.fromLocalFile(file_name))
        
    def add_new_tab(self, url=None, special_tab=False):
        new_tab = BrowserTab(special_tab)
        index = self.tabs.addTab(new_tab, "New Tab")
        self.tabs.setCurrentIndex(index)
        
        self.tabs.tabBar().setTabButton(index, QTabBar.RightSide, self.create_tab_close_button())
        
        if url:
            new_tab.web_view.setUrl(url)
        new_tab.web_view.urlChanged.connect(lambda url: self.update_url_bar(url))
        new_tab.web_view.titleChanged.connect(lambda title: self.update_tab_title(new_tab, title))

        if not special_tab:
            self.url_bar.setEnabled(True)
        return new_tab
        
    def current_tab(self):
        return self.tabs.currentWidget()
        
    def close_tab(self, index):
        if index >= 0:
            tab = self.tabs.widget(index)
            self.tabs.removeTab(index)
            if self.tabs.count() == 0:
                self.add_new_tab()
        
    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url:
            return
            
        if not url.startswith(('http://', 'https://', 'file://')):
            url = 'https://' + url
            
        self.current_tab().web_view.setUrl(QUrl(url))
            
    def perform_search(self):
        query = self.search_bar.text()
        if not query:
            return
            
        search_urls = {
            "Google": "https://www.google.com/search?q={}",
            "Yahoo": "https://search.yahoo.com/search?p={}"
        }
        
        search_url = search_urls[self.current_search_engine].format(query)
        self.current_tab().web_view.setUrl(QUrl(search_url))
        
    def update_url_bar(self, url):
        pass
        
    def update_tab_title(self, tab, title):
        index = self.tabs.indexOf(tab)
        if index >= 0:
            self.tabs.setTabText(index, title)

    def create_new_tab(self):
        new_tab = BrowserTab()
        index = self.tabs.addTab(new_tab, "New Tab")
        self.tabs.setCurrentIndex(index)
        
        self.tabs.tabBar().setTabButton(index, QTabBar.RightSide, self.create_tab_close_button())
        
        new_tab.web_view.urlChanged.connect(lambda url: self.update_url_bar(url))
        new_tab.web_view.titleChanged.connect(lambda title: self.update_tab_title(new_tab, title))

        self.url_bar.setEnabled(True)
        return new_tab

    def smooth_scroll(self, direction):
        scroll_value = 200  
        current_scroll = self.current_tab().web_view.page().scrollPosition()
        if direction == 'up':
            target_scroll = QPoint(current_scroll.x(), max(current_scroll.y() - scroll_value, 0))  
        elif direction == 'down':
            target_scroll = QPoint(current_scroll.x(), current_scroll.y() + scroll_value)
        else:
            return

        animation = QPropertyAnimation(self.current_tab().web_view.page(), b'scrollPosition')
        animation.setDuration(300)  
        animation.setStartValue(current_scroll)
        animation.setEndValue(target_scroll)
        animation.start(QAbstractAnimation.DeleteWhenStopped)

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

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos()
            
            # Get cursor position in screen coordinates
            cursor_pos = event.globalPos()
            frame_geo = self.frameGeometry()
            
            # Calculate distances from edges
            dist_left = abs(cursor_pos.x() - frame_geo.left())
            dist_right = abs(cursor_pos.x() - frame_geo.right())
            dist_top = abs(cursor_pos.y() - frame_geo.top())
            dist_bottom = abs(cursor_pos.y() - frame_geo.bottom())
            
            # Set resize flags based on proximity to edges
            if dist_left <= 10:
                self.resizing = True
                self.resize_edge = 'left'
                print("Left edge resize")
            elif dist_right <= 10:
                self.resizing = True
                self.resize_edge = 'right'
                print("Right edge resize")
            elif dist_top <= 10:
                self.resizing = True
                self.resize_edge = 'top'
                print("Top edge resize")
            elif dist_bottom <= 10:
                self.resizing = True
                self.resize_edge = 'bottom'
                print("Bottom edge resize")
            else:
                self.dragging = True
                print("Dragging")
        
    def mouseMoveEvent(self, event):
        if not event.buttons() & Qt.LeftButton:
            return
            
        current_pos = event.globalPos()
        delta = current_pos - self.drag_pos
        
        if self.resizing:
            print(f"Resizing with delta: {delta.x()}, {delta.y()}")
            current_geometry = self.geometry()
            new_geometry = QRect(current_geometry)
            
            if self.resize_edge == 'left':
                new_left = current_geometry.left() + delta.x()
                if current_geometry.right() - new_left >= self.minimumWidth():
                    new_geometry.setLeft(new_left)
                    
            elif self.resize_edge == 'right':
                new_right = current_geometry.right() + delta.x()
                if new_right - current_geometry.left() >= self.minimumWidth():
                    new_geometry.setRight(new_right)
                    
            elif self.resize_edge == 'top':
                new_top = current_geometry.top() + delta.y()
                if current_geometry.bottom() - new_top >= self.minimumHeight():
                    new_geometry.setTop(new_top)
                    
            elif self.resize_edge == 'bottom':
                new_bottom = current_geometry.bottom() + delta.y()
                if new_bottom - current_geometry.top() >= self.minimumHeight():
                    new_geometry.setBottom(new_bottom)
            
            print(f"New geometry: {new_geometry}")
            self.setGeometry(new_geometry)
            
        elif self.dragging:
            self.move(self.pos() + delta)
        
        self.drag_pos = current_pos

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            self.resizing = False
            self.resize_edge = None
            print("Released mouse button")
        
    def eventFilter(self, obj, event):
        # Double-click to maximize on tab bar
        if obj == self.tabs.tabBar():
            if event.type() == QEvent.MouseButtonDblClick:
                self.toggle_maximize()
                return True
            
            # Restore window dragging in tab bar area
            if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
                # Only start dragging if not on a tab
                if self.tabs.tabBar().tabAt(event.pos()) == -1:
                    self.dragging = True
                    self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
                    return True
            
            elif event.type() == QEvent.MouseButtonRelease:
                self.dragging = False
            
            elif event.type() == QEvent.MouseMove:
                if self.dragging and not self.isMaximized():
                    self.move(event.globalPos() - self.drag_position)
                    return True
        
        # Existing event filter logic for main window
        if event.type() == QEvent.MouseButtonPress and obj == self:
            if event.button() == Qt.LeftButton:
                if self.check_resize_area(event.pos()):
                    return True
                
                if event.pos().y() < 40:  
                    self.dragging = True
                    self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
                    event.accept()
                    return True
        
        elif event.type() == QEvent.MouseButtonRelease and obj == self:
            if event.button() == Qt.LeftButton:
                self.dragging = False
        
        elif event.type() == QEvent.MouseMove and obj == self:
            if self.dragging and not self.isMaximized():
                self.move(event.globalPos() - self.drag_position)
                event.accept()
                return True
        
        return super().eventFilter(obj, event)

    def check_resize_area(self, pos):
        x = pos.x()
        y = pos.y()
        width = self.width()
        height = self.height()
        
        # Increase resize border for easier grabbing
        border = 10
        
        # Check if we're in any resize area
        if x <= border:
            return 'left'
        elif x >= width - border:
            return 'right'
        elif y <= border:
            return 'top'
        elif y >= height - border:
            return 'bottom'
        return None

    def create_tab_close_button(self):
        close_button = QPushButton("×")
        close_button.setFixedSize(20, 20)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #ffffff;
                border: none;
                border-radius: 0px;
                font-size: 14px;
                font-weight: bold;
                margin: 0;
                padding: 0;
                height: 20px;
                max-height: 20px;
                min-height: 20px;
                width: 20px;
                max-width: 20px;
                min-width: 20px;
            }
            QPushButton:hover {
                background-color: #404040;
            }
        """)
        close_button.clicked.connect(lambda: self.close_tab(self.tabs.currentIndex()))
        return close_button

    def showMinimized(self):
        self.animation_type = 'minimize'
        current_pos = self.pos()
        end_pos = QPoint(current_pos.x(), current_pos.y() + self.height())
        
        self.slide_animation.setStartValue(current_pos)
        self.slide_animation.setEndValue(end_pos)
        self.slide_animation.start()

    def _handle_slide_finished(self):
        if self.animation_type == 'minimize':
            super().showMinimized()
            self.move(self.slide_animation.startValue())

    def close(self):
        super().close()

    def _handle_zoom_finished(self):
        if not self.isMaximized():
            self.showMaximized()
        else:
            self.showNormal()
            # Ensure we're at the exact pre-maximize geometry
            self.setGeometry(self.pre_maximize_geometry)

    def set_search_engine(self, engine):
        self.current_search_engine = engine
        self.search_bar.setPlaceholderText(f"Search with {engine}")
        
        # Update menu checkmarks
        search_menu = None
        for action in self.drift_btn.menu().actions():
            if action.menu() and action.text() == 'Search Engine':
                search_menu = action.menu()
                break
        
        if search_menu:
            for action in search_menu.actions():
                action.setChecked(action.text() == engine)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('WindowsVista')
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
