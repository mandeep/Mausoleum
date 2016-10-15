import sys

import pkg_resources

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QAction, QApplication, QDesktopWidget, QDialog, QFileDialog,
                             QFormLayout,
                             QGroupBox, QHBoxLayout, QLabel, QLineEdit, 
                             QMainWindow, QMenuBar, QStatusBar, QTabWidget,
                             QToolBar, QVBoxLayout, QWidget)


class CreateTomb(QWidget):
    """Creates the abstract widget to be used as a page."""

    def __init__(self, parent=None):
        """Initialize the create page's configuration and parameter groups."""
        super(CreateTomb, self).__init__(parent)
        self.layout = QVBoxLayout()

        self.tomb_group = QGroupBox('Tomb Configuration')
        self.tomb_name = QLineEdit()
        self.key_name = QLineEdit()
        self.key_password = QLineEdit()
        self.key_password.setEchoMode(QLineEdit.Password)
        self.tomb_layout = QFormLayout()
        self.tomb_layout.addRow('Tomb Name:', self.tomb_name)
        self.tomb_layout.addRow('Key Name:', self.key_name)
        self.tomb_layout.addRow('Key Password:', self.key_password)
        self.tomb_group.setLayout(self.tomb_layout)

        self.parameters_group = QGroupBox('Parameters')

        self.layout.addWidget(self.tomb_group)
        self.layout.addWidget(self.parameters_group)

        self.setLayout(self.layout)


class Mausoleum(QDialog):
    """Creates the main window that stores all of the widgets necessary for the application."""

    def __init__(self, parent=None):
        """Initialize the window size and title and instantiate the tab widget pages."""
        super(Mausoleum, self).__init__(parent)
        self.resize(600, 600)
        self.setWindowTitle('Mausoleum')
        window_icon = pkg_resources.resource_filename('mausoleum.images',
                                                      'ic_insert_drive_file_black_48dp_1x.png')
        self.setWindowIcon(QIcon(window_icon))

        create_page = CreateTomb()

        pages = QTabWidget()
        pages.addTab(create_page, 'Create')

        dialog_layout = QHBoxLayout()
        dialog_layout.addWidget(pages)

        self.setLayout(dialog_layout)


def main():
    application = QApplication(sys.argv)
    window = Mausoleum()
    desktop = QDesktopWidget().availableGeometry()
    width = (desktop.width() - window.width()) / 2
    height = (desktop.height() - window.height()) / 2
    window.show()
    window.move(width, height)
    sys.exit(application.exec_())
