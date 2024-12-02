from PyQt5.QtWidgets import QMainWindow, QApplication, QMenuBar, QMenu, QAction, QFileDialog
import sys

class MenuTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("driftapp.menubar.test")
        self.setGeometry(100, 100, 800, 600)
        
        menubar = self.menuBar()
        
        file_menu = menubar.addMenu('File')
        
        open_action = QAction('Open', self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
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
        
    def toggle_school_mode(self):
        if self.school_mode_action.isChecked():
            self.setWindowTitle("Menu.DiffTitle")
        else:
            self.setWindowTitle("MenuTest")
            
    def show_about(self):
        print("AboutTest")
        
    def open_file(self):
        QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MenuTestWindow()
    window.show()
    sys.exit(app.exec_())
