from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLineEdit, QPushButton, QTabWidget, QLabel, QToolButton, 
                            QComboBox, QMenuBar, QMenu, QAction, QListWidget, QDockWidget)
from PyQt5.QtCore import Qt
import sys

# Copy styles from driftapp.py
button_style = """
    QPushButton {
        background-color: #6E6D70;
        color: #ffffff;
        border-radius: 5px;
        border: 1px solid #000000;
        border-style: inset;
        border-width: 1px 1px 1px 1px;
        border-image: url(:/images/button-border.png) 1 1 1 1 / 1 1 1 1 / 0 0 0 0 / 0 0 0 0;
        font-size: 12px;
        min-width: 80px;
        min-height: 20px;
        padding: 5px 0px;
    }
    QPushButton:hover {
        background-color: #6E6D70;
    }
    QPushButton:pressed {
        background-color: #6E6D70;
    }
    QPushButton:checked {
        background-color: #6E6D70;
        border: 2px solid #606060;
    }
    QMessageBox QPushButton {
        background-color: #6E6D70;
        color: #ffffff;
        border-radius: 5px;
        border: 1px solid #000000;
        border-style: inset;
        border-width: 1px 1px 1px 1px;
        border-image: url(:/images/button-border.png) 1 1 1 1 / 1 1 1 1 / 0 0 0 0 / 0 0 0 0;
        font-size: 12px;
        min-width: 80px;
        min-height: 20px;
        padding: 5px 0px;
    }
    QMessageBox QPushButton:hover {
        background-color: #6E6D70;
    }
    QMessageBox QPushButton:pressed {
        background-color: #6E6D70;
    }
    QToolButton {
        background-color: #6E6D70;
        color: #ffffff;
        border-radius: 5px;
        border: 1px solid #000000;
        border-style: inset;
        border-width: 1px 1px 1px 1px;
        border-image: url(:/images/button-border.png) 1 1 1 1 / 1 1 1 1 / 0 0 0 0 / 0 0 0 0;
        font-size: 12px;
        min-width: 80px;
        min-height: 20px;
        padding: 5px 0px;
    }
    QToolButton:hover {
        background-color: #6E6D70;
    }
    QToolButton:pressed {
        background-color: #6E6D70;
    }
    QToolButton:checked {
        background-color: #6E6D70;
        border: 2px solid #606060;
    }
    QComboBox {
        background-color: #6E6D70;
        color: #ffffff;
        border-radius: 5px;
        border: 1px solid #000000;
        border-style: inset;
        border-width: 1px 1px 1px 1px;
        border-image: url(:/images/button-border.png) 1 1 1 1 / 1 1 1 1 / 0 0 0 0 / 0 0 0 0;
        font-size: 12px;
        min-width: 120px;
        min-height: 20px;
        padding: 5px;
    }
    QComboBox:hover {
        background-color: #6E6D70;
    }
    QComboBox:pressed {
        background-color: #6E6D70;
    }
    QComboBox QAbstractItemView {
        background-color: #6E6D70;
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
        color: #808080;
        padding: 8px;
        border-top: 1px solid #404040;
        border-radius: 2px 2px 0px 0px;
    }
    QTabBar::tab:selected {
        background-color: #404040;
        color: #ffffff;
        border: 2px solid #606060;
        border-radius: 5px;
    }
    QTabBar::tab:active {
        background-color: #505050;
        color: #ffffff;
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

class StyleTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("driftapp.pyqtstyles.test")
        self.setGeometry(100, 100, 800, 600)

        # Create menubar
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        file_menu.addAction('Test Action')

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Add TabWidget
        tabs = QTabWidget()
        tabs.addTab(QWidget(), "Tab 1")
        tabs.addTab(QWidget(), "Tab 2")
        layout.addWidget(tabs)

        # Create widget containers
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        
        # Add various buttons
        button_layout.addWidget(QPushButton("Regular Button"))
        
        tool_btn = QToolButton()
        tool_btn.setText("Tool Button")
        button_layout.addWidget(tool_btn)
        
        combo = QComboBox()
        combo.addItems(["Combo Item 1", "Combo Item 2", "Combo Item 3"])
        button_layout.addWidget(combo)
        
        layout.addWidget(button_container)

        # Add LineEdit
        line_edit = QLineEdit()
        line_edit.setPlaceholderText("This is a LineEdit")
        layout.addWidget(line_edit)

        # Add Label
        layout.addWidget(QLabel("This is a Label"))

        # Add ListWidget
        list_widget = QListWidget()
        list_widget.addItems(["List Item 1", "List Item 2", "List Item 3"])
        layout.addWidget(list_widget)

        # Add DockWidget
        dock = QDockWidget("Dock Widget", self)
        dock.setWidget(QLabel("Dock Content"))
        self.addDockWidget(Qt.RightDockWidgetArea, dock)

        # Apply styles
        app = QApplication.instance()
        app.setStyleSheet(dark_theme + button_style)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StyleTestWindow()
    window.show()
    sys.exit(app.exec_())
