from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTabWidget, QMessageBox, QMenu, QAction, QFileDialog, QTabBar
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt, QTimer, QPoint, QPropertyAnimation, QAbstractAnimation, QSize, QRect, QEvent
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

class BrowserTab(QWidget):
    def __init__(self, special_tab=False):
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
        self.special_tab = special_tab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drift")
        self.setGeometry(100, 100, 1024, 768)
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        self.dragging = False
        self.drag_pos = None
        
        self.resizing = False
        self.resize_edge = None
        self.resize_start = None
        self.resize_start_geo = None
        self.resize_border = 8
        self.resize_outer = 5
        
        self.setMouseTracking(True)

        icon_path = os.path.join(os.path.dirname(__file__), 'icon.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        self.activateWindow()
        self.raise_()
        
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: #1a1a1a; border: none;")
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

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
            }
            QTabBar::tab {
                background-color: transparent;
                color: #808080;
                padding: 0 35px 0 10px;
                height: 30px;
                min-height: 30px;
                max-height: 30px;
                border: none;
            }
            QTabBar::tab:hover:!selected {
                background-color: #252525;
            }
            QTabBar::tab:selected {
                background-color: #1f1f1f;
                color: #ffffff;
            }
            QTabBar::close-button {
                image: none;
                width: 30px;
                height: 30px;
                padding: 4px;
            }
            QTabBar::close-button:hover {
                background: #404040;
            }
            QTabBar::close-button:pressed {
                background: #666666;
            }
        """)

        # Create window controls for left corner
        left_corner = QWidget()
        left_layout = QHBoxLayout(left_corner)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)
        
        button_style = """
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
        """
        
        close_btn = QPushButton("×")
        close_btn.setStyleSheet(button_style + """
            QPushButton {
                background-color: #FF4141;
            }
            QPushButton:hover {
                background-color: #FF5252;
            }
        """)
        
        minimize_btn = QPushButton("−")
        minimize_btn.setStyleSheet(button_style + """
            QPushButton {
                background-color: #FFB900;
            }
            QPushButton:hover {
                background-color: #FFC926;
            }
        """)
        
        self.maximize_btn = QPushButton("⛶")
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
        
        self.drift_btn.setStyleSheet(button_style + """
            QPushButton {
                background-color: #1a1a2e;
            }
            QPushButton:hover {
                background-color: #252540;
            }
            QPushButton::menu-indicator {
                image: none;
            }
        """)

        left_layout.addWidget(close_btn)
        left_layout.addWidget(minimize_btn)
        left_layout.addWidget(self.maximize_btn)
        left_layout.addWidget(self.drift_btn)

        # Connect button signals
        close_btn.clicked.connect(self.close)
        minimize_btn.clicked.connect(self.showMinimized)
        self.maximize_btn.clicked.connect(self.toggle_maximize)
        
        # Create drift menu
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #2d2d2d;
                border: 1px solid #404040;
                border-radius: 8px;
                padding: 5px;
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
            QMenu::separator {
                height: 1px;
                background-color: #404040;
                margin: 5px 15px;
            }
        """)

        drift_pad_action = QAction("DriftPad", self)
        drift_pad_action.triggered.connect(self.open_drift_pad)
        menu.addAction(drift_pad_action)
        
        open_action = QAction('Open', self)
        open_action.triggered.connect(self.open_file)
        menu.addAction(open_action)

        menu.addSeparator()
        
        about_action = QAction('About Drift', self)
        about_action.triggered.connect(self.show_about)
        menu.addAction(about_action)
        
        quit_action = QAction('Quit', self)
        quit_action.triggered.connect(self.close)
        menu.addAction(quit_action)
        
        self.drift_btn.setMenu(menu)

        # Set window controls in left corner
        self.tabs.setCornerWidget(left_corner, Qt.TopLeftCorner)

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
            }
            QPushButton:hover {
                background-color: #404040;
            }
        """)
        self.new_tab_btn.clicked.connect(self.add_new_tab)
        right_layout.addWidget(self.new_tab_btn)
        self.tabs.setCornerWidget(right_corner, Qt.TopRightCorner)

        # Add everything to main layout
        layout.addWidget(self.tabs)

        nav_bar = QWidget()
        nav_layout = QHBoxLayout()
        nav_layout.setContentsMargins(2, 2, 2, 2)
        nav_bar.setLayout(nav_layout)
        
        nav_button_style = """
            QPushButton {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #404040;
                border-radius: 3px;
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
        
        self.back_btn = QPushButton("←")
        self.back_btn.setStyleSheet(nav_button_style)
        self.forward_btn = QPushButton("→")
        self.forward_btn.setStyleSheet(nav_button_style)
        self.reload_btn = QPushButton("⟳")
        self.reload_btn.setStyleSheet(nav_button_style)
        
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Enter URL (doesn't need HTTPS prefix)")
        
        nav_layout.addWidget(self.back_btn)
        nav_layout.addWidget(self.forward_btn)
        nav_layout.addWidget(self.reload_btn)
        nav_layout.addWidget(self.url_bar)
        
        layout.addWidget(nav_bar)
        
        self.add_new_tab()
        
        self.back_btn.clicked.connect(lambda: self.current_tab().web_view.back())
        self.forward_btn.clicked.connect(lambda: self.current_tab().web_view.forward())
        self.reload_btn.clicked.connect(lambda: self.current_tab().web_view.reload())
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        
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
        
    def open_drift_pad(self):
        notes_path = os.path.join(os.path.dirname(__file__), 'Assets', 'notesapp.html')
        new_tab = self.add_new_tab(QUrl.fromLocalFile(notes_path), special_tab=True)
        self.url_bar.setEnabled(False)

    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
            self.maximize_btn.setText("⛶")  
        else:
            self.showMaximized()
            self.maximize_btn.setText("❐")  

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
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
            if not self.current_tab().special_tab:
                self.url_bar.setEnabled(True)
        else:
            sys.exit(1)
        
    def navigate_to_url(self):
        url = self.url_bar.text()
        if url.startswith('drift:'):
            drift_command = url[6:].lower()
            if drift_command == 'about':
                self.show_about()
            elif drift_command == 'progress':
                self.add_new_tab(QUrl('https://github.com/users/DriftBR/projects/1/views/1'))
            elif drift_command == 'source':
                self.add_new_tab(QUrl('https://github.com/DriftBR/DriftBR'))
            elif drift_command == 'try':
                self.add_new_tab(QUrl.fromLocalFile(os.path.join(os.path.dirname(__file__), 'Assets', 'TryDrift.html')))
            else:
                QMessageBox.warning(self, 'Invalid Command', f'"drift:{drift_command}" is invalid dude', QMessageBox.Ok)
            self.url_bar.clear()
            return
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url 
        self.current_tab().web_view.setUrl(QUrl(url))
        self.url_bar.clear()
        
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

    def check_resize_area(self, pos):
        geo = self.geometry()
        total_border = self.resize_border + self.resize_outer
        
        global_pos = self.mapToGlobal(pos)
        window_rect = self.frameGeometry()
        
        left_dist = abs(global_pos.x() - window_rect.left())
        right_dist = abs(global_pos.x() - window_rect.right())
        top_dist = abs(global_pos.y() - window_rect.top())
        bottom_dist = abs(global_pos.y() - window_rect.bottom())
        
        left = left_dist <= total_border
        right = right_dist <= total_border
        top = top_dist <= total_border
        bottom = bottom_dist <= total_border
        
        edges = []
        if left: edges.append('left')
        if right: edges.append('right')
        if top: edges.append('top')
        if bottom: edges.append('bottom')
        
        return edges

    def get_resize_cursor(self, edges):
        if not edges:
            return Qt.ArrowCursor
        
        if 'top' in edges and 'left' in edges:
            return Qt.SizeFDiagCursor
        if 'top' in edges and 'right' in edges:
            return Qt.SizeBDiagCursor
        if 'bottom' in edges and 'left' in edges:
            return Qt.SizeBDiagCursor
        if 'bottom' in edges and 'right' in edges:
            return Qt.SizeFDiagCursor
        if 'left' in edges or 'right' in edges:
            return Qt.SizeHorCursor
        if 'top' in edges or 'bottom' in edges:
            return Qt.SizeVerCursor
        
        return Qt.ArrowCursor

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            edges = self.check_resize_area(event.pos())
            
            if edges:
                self.resizing = True
                self.resize_start = event.globalPos()
                self.resize_start_geo = self.geometry()
                self.resize_edge = edges
            else:
                self.dragging = True
                self.drag_pos = event.globalPos()
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            self.resizing = False
            self.resize_edge = None
            event.accept()

    def mouseMoveEvent(self, event):
        if self.resizing and event.buttons() & Qt.LeftButton:
            delta = event.globalPos() - self.resize_start
            new_geo = QRect(self.resize_start_geo)
            
            if 'left' in self.resize_edge:
                new_geo.setLeft(new_geo.left() + delta.x())
            if 'right' in self.resize_edge:
                new_geo.setRight(self.resize_start_geo.right() + delta.x())
            if 'top' in self.resize_edge:
                new_geo.setTop(new_geo.top() + delta.y())
            if 'bottom' in self.resize_edge:
                new_geo.setBottom(self.resize_start_geo.bottom() + delta.y())
            
            min_width = max(self.minimumWidth(), 400)
            min_height = max(self.minimumHeight(), 300)
            
            if new_geo.width() >= min_width and new_geo.height() >= min_height:
                self.setGeometry(new_geo)
                
        elif self.dragging and event.buttons() & Qt.LeftButton:
            delta = event.globalPos() - self.drag_pos
            new_pos = self.pos() + delta
            self.move(new_pos)
            self.drag_pos = event.globalPos()
        else:
            edges = self.check_resize_area(event.pos())
            self.setCursor(self.get_resize_cursor(edges))
            
        event.accept()

    def eventFilter(self, obj, event):
        if obj == QApplication.instance() and event.type() == QEvent.KeyPress:
            modifiers = event.modifiers()
            key = event.key()
            
            if modifiers & Qt.MetaModifier:
                if key == Qt.Key_Up:
                    self.showMaximized() if not self.isMaximized() else self.showNormal()
                    return True
                elif key == Qt.Key_Down:
                    if self.isMaximized():
                        self.showNormal()
                    else:
                        self.showMinimized()
                    return True
                elif key == Qt.Key_Left:
                    if not self.isMaximized():
                        screen = QApplication.primaryScreen().availableGeometry()
                        self.setGeometry(screen.left(), screen.top(),
                                       screen.width() // 2, screen.height())
                    return True
                elif key == Qt.Key_Right:
                    if not self.isMaximized():
                        screen = QApplication.primaryScreen().availableGeometry()
                        self.setGeometry(screen.center().x(), screen.top(),
                                       screen.width() // 2, screen.height())
                    return True
        
        elif obj == self.tabs.tabBar():
            if event.type() == event.MouseButtonPress:
                if event.button() == Qt.LeftButton:
                    tab_pos = obj.tabAt(event.pos())
                    if tab_pos >= 0:  
                        obj.setCurrentIndex(tab_pos)
                        return False  
                    self.dragging = True
                    self.drag_pos = event.globalPos()
                    return True
            elif event.type() == event.MouseButtonRelease:
                if event.button() == Qt.LeftButton:
                    self.dragging = False
                    return False  
            elif event.type() == event.MouseMove:
                if self.dragging and event.buttons() & Qt.LeftButton:
                    delta = event.globalPos() - self.drag_pos
                    new_pos = self.pos() + delta
                    self.move(new_pos)
                    self.drag_pos = event.globalPos()
                    return True
        
        return super().eventFilter(obj, event)

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('WindowsVista')
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())