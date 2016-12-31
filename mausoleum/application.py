import os
import pkg_resources
import shutil
import sys

from appdirs import AppDirs
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QCheckBox, QDesktopWidget, QDialog, QFileDialog,
                             QFormLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QListWidget,
                             QPushButton, QSpinBox, QTabWidget, QVBoxLayout, QWidget)
import pytoml

from mausoleum import wrapper


class CreateTomb(QWidget):
    """Creates the abstract widget to be used as a create page."""

    def __init__(self, path, parent=None):
        """Initialize the create page's configuration and parameter groups."""
        super(CreateTomb, self).__init__(parent)

        self.path = path

        layout = QVBoxLayout()

        tomb_group = QGroupBox('Create Tomb')

        self.tomb_name = QLineEdit()
        tomb_name_button = QPushButton('Select Path')
        tomb_name_layout = QHBoxLayout()
        tomb_name_layout.addWidget(self.tomb_name)
        tomb_name_layout.addWidget(tomb_name_button)

        self.key_name = QLineEdit()
        key_name_button = QPushButton('Select Path')
        key_name_layout = QHBoxLayout()
        key_name_layout.addWidget(self.key_name)
        key_name_layout.addWidget(key_name_button)

        self.key_password = QLineEdit()
        self.key_password.setEchoMode(QLineEdit.Password)
        self.confirm_password = QLineEdit()
        self.confirm_password.setEchoMode(QLineEdit.Password)
        self.sudo_password = QLineEdit()
        self.sudo_password.setEchoMode(QLineEdit.Password)

        tomb_layout = QFormLayout()
        tomb_layout.addRow('Tomb Name:', self.tomb_name)
        tomb_layout.addRow('Key Name:', self.key_name)
        tomb_layout.addRow('Key Password:', self.key_password)
        tomb_layout.addRow('Confirm Password:', self.confirm_password)
        tomb_layout.addRow('Sudo Password:', self.sudo_password)
        tomb_group.setLayout(tomb_layout)

        parameters_group = QGroupBox('Parameters')

        size_box_layout = QHBoxLayout()
        size_box_label = QLabel('Size (MB):')
        self.size_box = QSpinBox()
        self.size_box.setMaximum(999999)
        self.size_box.setMinimum(10)
        self.size_box.setFixedWidth(100)
        size_box_layout.addWidget(size_box_label)
        size_box_layout.addWidget(self.size_box)
        size_box_layout.setSpacing(0)

        kdf_box_layout = QHBoxLayout()
        kdf_box_label = QLabel('KDF Iterations:')
        self.kdf_box = QSpinBox()
        self.kdf_box.setFixedWidth(100)
        kdf_box_layout.addWidget(kdf_box_label)
        kdf_box_layout.addWidget(self.kdf_box)

        spinbox_layout = QVBoxLayout()
        spinbox_layout.addLayout(size_box_layout)
        spinbox_layout.addLayout(kdf_box_layout)
        spinbox_layout.setAlignment(Qt.AlignLeft)

        open_checkbox_layout = QHBoxLayout()
        open_checkbox_label = QLabel('Open Upon Creation:')
        self.open_checkbox = QCheckBox()
        open_checkbox_layout.addWidget(open_checkbox_label)
        open_checkbox_layout.addWidget(self.open_checkbox)

        random_checkbox_layout = QHBoxLayout()
        random_checkbox_label = QLabel('Random Integer Key:')
        self.random_checkbox = QCheckBox()
        random_checkbox_layout.addWidget(random_checkbox_label)
        random_checkbox_layout.addWidget(self.random_checkbox)

        checkbox_layout = QVBoxLayout()
        checkbox_layout.addLayout(open_checkbox_layout)
        checkbox_layout.addLayout(random_checkbox_layout)
        checkbox_layout.setAlignment(Qt.AlignLeft)

        parameters_layout = QHBoxLayout()
        parameters_layout.addLayout(spinbox_layout)
        parameters_layout.addLayout(checkbox_layout)

        parameters_group.setLayout(parameters_layout)

        self.create_button = QPushButton('Create Tomb')
        self.create_button.setFixedWidth(200)

        self.message = QLabel()

        if shutil.which('tomb') is None:
            self.message.setText('Warning: Tomb Installation Not Found; '
                                 'Set Tomb Path On Config Tab')

        layout.addWidget(tomb_group)
        layout.addWidget(parameters_group)
        layout.addWidget(self.create_button, alignment=Qt.AlignCenter)
        layout.addWidget(self.message, alignment=Qt.AlignCenter)
        layout.addStretch(1)

        self.setLayout(layout)

        self.tomb_name.textChanged.connect(self.fill_key_name)
        self.create_button.clicked.connect(self.create_defined_tomb)

    def fill_key_name(self):
        """Fill the key name text box according to the text of the tomb name text box."""
        self.key_name.setText(self.tomb_name.text() + '.key')

    def create_defined_tomb(self):
        """Create the defined tomb when Create Tomb is clicked.

        The key's password and sudo password are not stored as strings so that the only
        place passwords are stored is in QLineEdit. QLineEdit will clear the passwords,
        however we must make sure that the application is not stored in swap.
        """
        if self.key_password.text() == self.confirm_password.text():

            dig_command = wrapper.dig_tomb(self.tomb_name.text(), self.size_box.value())

            forge_command = wrapper.forge_tomb(self.key_name.text(),
                                               self.key_password.text(),
                                               self.path,
                                               kdf=self.kdf_box.value(),
                                               sudo=self.sudo_password.text(),
                                               debug=self.random_checkbox.isChecked())

            lock_command = wrapper.lock_tomb(self.tomb_name.text(),
                                             self.key_name.text(),
                                             self.key_password.text(),
                                             self.path,
                                             sudo=self.sudo_password.text())

            if (dig_command == 0 and forge_command[0] is not None and
                    lock_command[0] is not None):
                self.message.setText('Tomb Created Successfully')

                if self.open_checkbox.isChecked():
                    open_command = wrapper.open_tomb(self.tomb_name.text(),
                                                     self.key_name.text(),
                                                     self.key_password.text(),
                                                     self.path,
                                                     sudo=self.sudo_password.text())

                    if open_command[0] is not None:
                        self.message.setText('Tomb Opened Successfully')

        else:
            self.message.setText('Key Passwords Do Not Match')
            self.key_password.clear()
            self.confirm_password.clear()


class OpenTomb(QWidget):
    """Creates the abstract widget to be used as an open page."""

    def __init__(self, path, parent=None):
        """Initialize the open page's configuration group."""
        super(OpenTomb, self).__init__(parent)

        self.path = path

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

        self.open_button = QPushButton('Open Tomb')
        self.open_button.setFixedWidth(200)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.open_button, alignment=Qt.AlignCenter)
        button_layout.setContentsMargins(25, 25, 25, 25)

        self.message = QLabel()

        parameters_group = QGroupBox('Mount Options')

        read_only_layout = QHBoxLayout()
        read_only_label = QLabel('Read Only:')
        self.read_only_checkbox = QCheckBox()
        read_only_layout.addWidget(read_only_label)
        read_only_layout.addWidget(self.read_only_checkbox)

        checkbox_layout = QVBoxLayout()
        checkbox_layout.addLayout(read_only_layout)
        checkbox_layout.setAlignment(Qt.AlignLeft)

        parameters_layout = QHBoxLayout()

        parameters_layout.addLayout(checkbox_layout)

        parameters_group.setLayout(parameters_layout)

        layout.addWidget(open_group)
        layout.addWidget(parameters_group)
        layout.addLayout(button_layout)
        layout.addWidget(self.message, alignment=Qt.AlignCenter)
        layout.addStretch(1)

        self.setLayout(layout)

        tomb_path_button.clicked.connect(self.select_tomb_path)
        key_path_button.clicked.connect(self.select_key_path)
        self.open_button.clicked.connect(self.open_selected_tomb)

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
        """Open the selected tomb with the selected key, key password, and sudo password.

        The key's password and sudo password are not stored as strings so that the only
        place passwords are stored is in QLineEdit. QLineEdit will clear the passwords,
        however we must make sure that the application is not stored in swap.
        """
        open_command = wrapper.open_tomb(self.tomb_path.text(),
                                         self.key_path.text(),
                                         self.key_password.text(),
                                         self.path,
                                         read_only=self.read_only_checkbox.isChecked(),
                                         sudo=self.sudo_password.text())
        if open_command[0] is not None:
            self.message.setText('Tomb Opened Successfully')
            self.tomb_path.clear()
            self.key_path.clear()
            self.key_password.clear()
            self.sudo_password.clear()


class CloseTomb(QWidget):
    """Creates the abstract widget to be used as a close page."""

    def __init__(self, path, parent=None):
        """Initialize the close page's configuration group."""
        super(CloseTomb, self).__init__(parent)

        self.path = path

        layout = QVBoxLayout()

        close_group = QGroupBox('Close Tomb')

        close_layout = QVBoxLayout()
        self.close_all_button = QPushButton('Close All Tombs')
        self.close_all_button.setFixedWidth(200)
        self.force_close_button = QPushButton('Force Close Tombs')
        self.force_close_button.setFixedWidth(200)
        close_layout.addWidget(self.close_all_button, alignment=Qt.AlignCenter)
        close_layout.addWidget(self.force_close_button, alignment=Qt.AlignCenter)

        close_group.setLayout(close_layout)

        layout.addWidget(close_group)
        layout.addStretch(1)

        self.setLayout(layout)

        self.close_all_button.clicked.connect(lambda: wrapper.close_tombs(self.path))
        self.force_close_button.clicked.connect(lambda: wrapper.slam_tombs(self.path))


class ListTomb(QWidget):
    """Creates the abstract widget to be used as a list page."""

    def __init__(self, path, parent=None):
        """Initialize the list page's configuration group."""
        super(ListTomb, self).__init__(parent)

        self.path = path

        layout = QVBoxLayout()

        list_group = QGroupBox('Active Tombs')

        list_layout = QVBoxLayout()
        self.tomb_list = QListWidget()

        self.update_list_button = QPushButton('Update')
        self.update_list_button.setFixedWidth(200)

        list_layout.addWidget(self.tomb_list)
        list_layout.addWidget(self.update_list_button, alignment=Qt.AlignCenter)

        list_group.setLayout(list_layout)
        layout.addWidget(list_group)
        self.setLayout(layout)

        self.update_list_button.clicked.connect(self.update_list_items)

    def update_list_items(self):
        """Clear the list and add any active tombs."""
        self.tomb_list.clear()
        for line in wrapper.list_tombs(self.path):
            self.tomb_list.addItem(line)


class ConfigTomb(QWidget):
    """Creates the abstract widget to be used as a config page."""

    def __init__(self, parent=None):
        """Initialize the config page's configuration group."""
        super(ConfigTomb, self).__init__(parent)

        config_directory = AppDirs('mausoleum', 'Mandeep').user_config_dir

        if not os.path.exists(config_directory):
            os.makedirs(config_directory)

        settings = pkg_resources.resource_filename(__name__, 'settings.toml')
        with open(settings) as default_config:
            default_config = default_config.read()

        self.user_config_file = os.path.join(config_directory, 'settings.toml')
        if not os.path.isfile(self.user_config_file):
            with open(self.user_config_file, 'a') as new_config_file:
                new_config_file.write(default_config)

        with open(self.user_config_file) as conffile:
            self.config = pytoml.load(conffile)

        config_box = QGroupBox("Configure Mausoleum")

        self.tomb_path_label = QLabel('Tomb Path', self)
        self.tomb_path_line = QLineEdit()
        self.tomb_path_line.setReadOnly(True)
        self.tomb_path_button = QPushButton('Select Path')

        self.tomb_path_button.clicked.connect(lambda: self.select_tomb_install_path(self.config))

        tomb_path_layout = QVBoxLayout()

        tomb_path_config_layout = QHBoxLayout()
        tomb_path_config_layout.addWidget(self.tomb_path_label)
        tomb_path_config_layout.addWidget(self.tomb_path_line)
        tomb_path_config_layout.addWidget(self.tomb_path_button)

        tomb_path_layout.addLayout(tomb_path_config_layout)

        config_box.setLayout(tomb_path_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(config_box)
        main_layout.addStretch(1)
        self.setLayout(main_layout)

        self.set_tomb_path(self.config)

    def select_tomb_install_path(self, config):
        """Select Tomb's installation path."""
        tomb_install_path = QFileDialog.getExistingDirectory(
                            self, 'Select Tomb Installation Path')

        if tomb_install_path:
            self.tomb_path_line.setText(tomb_install_path)

            config['configuration']['path'] = tomb_install_path

            with open(self.user_config_file, 'w') as conffile:
                pytoml.dump(conffile, config)

    def set_tomb_path(self, config):
        """Set Tomb's current installation path."""
        current_tomb_path = config['configuration']['path']
        if os.path.isdir(current_tomb_path):
            self.tomb_path_line.setText(current_tomb_path)
        else:
            self.tomb_path_line.setText(shutil.which('tomb'))


class Mausoleum(QDialog):
    """Creates the main window that stores all of the widgets necessary for the application."""

    def __init__(self, parent=None):
        """Initialize the window size and title and instantiate the tab widget pages."""
        super(Mausoleum, self).__init__(parent)
        self.resize(600, 600)
        self.setWindowTitle('Mausoleum')
        window_icon = pkg_resources.resource_filename('mausoleum.images',
                                                      'ic_vpn_key_black_48dp_1x.png')
        self.setWindowIcon(QIcon(window_icon))

        self.tomb_current_path = ConfigTomb().tomb_path_line.text()

        self.create_page = CreateTomb(self.tomb_current_path)
        self.open_page = OpenTomb(self.tomb_current_path)
        self.close_page = CloseTomb(self.tomb_current_path)
        self.list_page = ListTomb(self.tomb_current_path)
        self.config_page = ConfigTomb()

        self.pages = QTabWidget()
        self.pages.addTab(self.create_page, 'Create')
        self.pages.addTab(self.open_page, 'Open')
        self.pages.addTab(self.close_page, 'Close')
        self.pages.addTab(self.list_page, 'List')
        self.pages.addTab(self.config_page, 'Config')

        dialog_layout = QHBoxLayout()
        dialog_layout.addWidget(self.pages)

        self.setLayout(dialog_layout)

        self.create_page.create_button.clicked.connect(self.update_list_items)
        self.open_page.open_button.clicked.connect(self.update_list_items)
        self.close_page.close_all_button.clicked.connect(self.update_list_items)
        self.close_page.force_close_button.clicked.connect(self.update_list_items)

    def update_list_items(self):
        """Update the list of active tombs whenever a tomb is opened or closed."""
        QTimer.singleShot(3000, self.list_page.update_list_items)


def main():
    application = QApplication(sys.argv)
    window = Mausoleum()
    desktop = QDesktopWidget().availableGeometry()
    width = (desktop.width() - window.width()) / 2
    height = (desktop.height() - window.height()) / 2
    window.show()
    window.move(width, height)
    sys.exit(application.exec_())
