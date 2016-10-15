import sys

import pkg_resources

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QDesktopWidget, QDialog, QFileDialog,
                             QFormLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QTabWidget, QVBoxLayout, QWidget)

from mausoleum import wrapper


class CreateTomb(QWidget):
    """Creates the abstract widget to be used as a create page."""

    def __init__(self, parent=None):
        """Initialize the create page's configuration and parameter groups."""
        super(CreateTomb, self).__init__(parent)
        layout = QVBoxLayout()

        tomb_group = QGroupBox('Tomb Configuration')
        tomb_name = QLineEdit()
        key_name = QLineEdit()
        key_password = QLineEdit()
        key_password.setEchoMode(QLineEdit.Password)
        tomb_layout = QFormLayout()
        tomb_layout.addRow('Tomb Name:', tomb_name)
        tomb_layout.addRow('Key Name:', key_name)
        tomb_layout.addRow('Key Password:', key_password)
        tomb_group.setLayout(tomb_layout)

        parameters_group = QGroupBox('Parameters')

        layout.addWidget(tomb_group)
        layout.addWidget(parameters_group)

        self.setLayout(layout)


class OpenTomb(QWidget):
    """Creates the abstract widget to be used as an open page."""

    def __init__(self, parent=None):
        """Initialize the open page's configuration group."""
        super(OpenTomb, self).__init__(parent)

        layout = QVBoxLayout()

        open_group = QGroupBox('Open Tomb')

        self.tomb_path = QLineEdit()
        tomb_path_button = QPushButton('Select Path')
        tomb_path_layout = QHBoxLayout()
        tomb_path_layout.addWidget(self.tomb_path)
        tomb_path_layout.addWidget(tomb_path_button)

        self.key_path = QLineEdit()
        key_path_button = QPushButton('Select Path')
        key_path_layout = QHBoxLayout()
        key_path_layout.addWidget(self.key_path)
        key_path_layout.addWidget(key_path_button)

        self.key_password = QLineEdit()
        self.key_password.setEchoMode(QLineEdit.Password)
        self.sudo_password = QLineEdit()
        self.sudo_password.setEchoMode(QLineEdit.Password)

        open_layout = QFormLayout()
        open_layout.addRow('Tomb Path:', tomb_path_layout)
        open_layout.addRow('Key Path:', key_path_layout)
        open_layout.addRow('Key Password:', self.key_password)
        open_layout.addRow('Sudo Password:', self.sudo_password)
        open_group.setLayout(open_layout)

        open_button = QPushButton('Open Tomb')
        open_button.setFixedWidth(200)
        close_button = QPushButton('Close Tomb')
        close_button.setFixedWidth(200)
        button_layout = QHBoxLayout()
        button_layout.addWidget(open_button, alignment=Qt.AlignCenter)
        button_layout.addWidget(close_button, alignment=Qt.AlignCenter)

        self.success_message = QLabel()

        layout.addWidget(open_group)
        layout.addLayout(button_layout)
        layout.addWidget(self.success_message, alignment=Qt.AlignCenter)

        self.setLayout(layout)

        tomb_path_button.clicked.connect(self.select_tomb_path)
        key_path_button.clicked.connect(self.select_key_path)
        open_button.clicked.connect(self.open_selected_tomb)
        close_button.clicked.connect(self.close_selected_tomb)

    def select_tomb_path(self):
        """Select the path of the tomb to open."""
        filename, ok = QFileDialog.getOpenFileName(self, 'Tomb Container')

        if ok:
            self.tomb_path.setText(filename)

    def select_key_path(self):
        """Select the path of the key to open."""
        filename, ok = QFileDialog.getOpenFileName(self, 'Tomb Container')

        if ok:
            self.key_path.setText(filename)

    def open_selected_tomb(self):
        """Open the selected tomb with the selected key, key password, and sudo password."""
        name = self.tomb_path.text()
        key = str(self.key_path.text())
        password = self.key_password.text()
        sudo = self.sudo_password.text()
        open_command = wrapper.open_tomb(name, key, password, sudo)
        if open_command[0] is not None:
            self.success_message.setText('Tomb Opened Successfully.')

    def close_selected_tomb(self):
        """Close the opened tomb."""
        close_command = wrapper.close_tomb()
        if close_command.returncode == 0:
            self.success_message.setText('Tomb Closed Successfully.')


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
        open_page = OpenTomb()

        pages = QTabWidget()
        pages.addTab(create_page, 'Create')
        pages.addTab(open_page, 'Open')

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
