import os
import importlib.resources
import shutil
import sys

from appdirs import AppDirs
from PyQt5.QtCore import pyqtSignal, Qt, QTimer
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
        self.debug = False

        layout = QVBoxLayout()

        tomb_group = QGroupBox('Create Tomb')

        self.tomb_name = QLineEdit()
        tomb_name_layout = QHBoxLayout()
        tomb_name_layout.addWidget(self.tomb_name)

        self.key_name = QLineEdit()
        key_name_layout = QHBoxLayout()
        key_name_layout.addWidget(self.key_name)

        self.key_password = QLineEdit()
        self.key_password.setEchoMode(QLineEdit.Password)
        self.confirm_password = QLineEdit()
        self.confirm_password.setEchoMode(QLineEdit.Password)
        self.sudo_password = QLineEdit()
        self.sudo_password.setEchoMode(QLineEdit.Password)

        self.tomb_layout = QFormLayout()
        self.tomb_layout.addRow('Tomb Name:', self.tomb_name)
        self.tomb_layout.addRow('Key Name:', self.key_name)
        self.tomb_layout.addRow('Key Password:', self.key_password)
        self.tomb_layout.addRow('Confirm Password:', self.confirm_password)
        self.tomb_layout.addRow('Sudo Password:', self.sudo_password)

        tomb_group.setLayout(self.tomb_layout)

        parameters_group = QGroupBox('Parameters')

        size_box_layout = QHBoxLayout()
        size_box_label = QLabel('Size (MB):')
        self.size_box = QSpinBox()
        self.size_box.setMaximum(999999)
        self.size_box.setMinimum(10)
        self.size_box.setFixedWidth(100)
        size_box_label.setBuddy(self.size_box)
        size_box_layout.addWidget(size_box_label)
        size_box_layout.addWidget(self.size_box)
        size_box_layout.setSpacing(0)

        kdf_box_layout = QHBoxLayout()
        kdf_box_label = QLabel('KDF Iterations:')
        self.kdf_box = QSpinBox()
        self.kdf_box.setFixedWidth(100)
        kdf_box_label.setBuddy(self.kdf_box)
        kdf_box_layout.addWidget(kdf_box_label)
        kdf_box_layout.addWidget(self.kdf_box)

        spinbox_layout = QVBoxLayout()
        spinbox_layout.addLayout(size_box_layout)
        spinbox_layout.addLayout(kdf_box_layout)
        spinbox_layout.setAlignment(Qt.AlignLeft)

        checkbox_layout = QVBoxLayout()
        self.open_checkbox = QCheckBox('Open Upon Creation')
        self.random_checkbox = QCheckBox('Random Integer Key')
        checkbox_layout.addWidget(self.open_checkbox)
        checkbox_layout.addWidget(self.random_checkbox)
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
                                                     debug=self.debug,
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
        self.debug = False

        layout = QVBoxLayout()

        open_group = QGroupBox('Open Tomb')

        self.tomb_path = QLineEdit()
        self.tomb_path_button = QPushButton('Select Path')
        tomb_path_layout = QHBoxLayout()
        tomb_path_layout.addWidget(self.tomb_path)
        tomb_path_layout.addWidget(self.tomb_path_button)

        self.key_path = QLineEdit()
        self.key_path_button = QPushButton('Select Path')
        key_path_layout = QHBoxLayout()
        key_path_layout.addWidget(self.key_path)
        key_path_layout.addWidget(self.key_path_button)

        self.key_password = QLineEdit()
        self.key_password.setEchoMode(QLineEdit.Password)
        self.sudo_password = QLineEdit()
        self.sudo_password.setEchoMode(QLineEdit.Password)

        self.open_layout = QFormLayout()
        self.open_layout.addRow('Tomb Path:', tomb_path_layout)
        self.open_layout.addRow('Key Path:', key_path_layout)
        self.open_layout.addRow('Key Password:', self.key_password)
        self.open_layout.addRow('Sudo Password:', self.sudo_password)
        open_group.setLayout(self.open_layout)

        self.open_button = QPushButton('Open Tomb')
        self.open_button.setFixedWidth(200)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.open_button, alignment=Qt.AlignCenter)
        button_layout.setContentsMargins(25, 25, 25, 25)

        self.message = QLabel()

        parameters_group = QGroupBox('Mount Options')

        checkbox_layout = QHBoxLayout()
        self.read_only_checkbox = QCheckBox('Read Only')
        checkbox_layout.addWidget(self.read_only_checkbox)
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

        self.tomb_path_button.clicked.connect(self.select_tomb_path)
        self.key_path_button.clicked.connect(self.select_key_path)
        self.open_button.clicked.connect(self.open_selected_tomb)

    def select_tomb_path(self):
        """Select the path of the tomb to open.

        If the tomb's key is in the same directory as the tomb and follows the
        pattern of file.tomb.key, then the key's path is filled in its text box.
        """
        filename, ok = QFileDialog.getOpenFileName(self, 'Tomb Container')

        if ok:
            self.tomb_path.setText(filename)

            key = "{}.key" .format(self.tomb_path.text())

            if os.path.isfile(key):
                self.key_path.setText(key)

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
                                         debug=self.debug,
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


class ResizeTomb(QWidget):
    """Creates the abstract widget to be used as a resize page."""

    def __init__(self, path, parent=None):
        """Initialize the resize page's configuration group."""
        super(ResizeTomb, self).__init__(parent)

        self.path = path
        self.debug = False

        layout = QVBoxLayout()

        resize_group = QGroupBox('Resize Tomb')

        self.tomb_path = QLineEdit()
        self.tomb_path_button = QPushButton('Select Path')
        tomb_path_layout = QHBoxLayout()
        tomb_path_layout.addWidget(self.tomb_path)
        tomb_path_layout.addWidget(self.tomb_path_button)

        self.key_path = QLineEdit()
        self.key_path_button = QPushButton('Select Path')
        key_path_layout = QHBoxLayout()
        key_path_layout.addWidget(self.key_path)
        key_path_layout.addWidget(self.key_path_button)

        self.key_password = QLineEdit()
        self.key_password.setEchoMode(QLineEdit.Password)
        self.sudo_password = QLineEdit()
        self.sudo_password.setEchoMode(QLineEdit.Password)

        self.resize_layout = QFormLayout()
        self.resize_layout.addRow('Tomb Path:', tomb_path_layout)
        self.resize_layout.addRow('Key Path:', key_path_layout)
        self.resize_layout.addRow('Key Password:', self.key_password)
        self.resize_layout.addRow('Sudo Password:', self.sudo_password)
        resize_group.setLayout(self.resize_layout)

        self.resize_button = QPushButton('Resize Tomb')
        self.resize_button.setFixedWidth(200)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.resize_button, alignment=Qt.AlignCenter)
        button_layout.setContentsMargins(25, 25, 25, 25)

        self.message = QLabel()

        parameters_group = QGroupBox('Parameters')

        size_box_layout = QHBoxLayout()
        size_box_label = QLabel('Size (MB):')
        self.size_box = QSpinBox()
        self.size_box.setMaximum(999999)
        self.size_box.setMinimum(10)
        self.size_box.setFixedWidth(100)
        size_box_label.setBuddy(self.size_box)
        size_box_layout.addWidget(size_box_label)
        size_box_layout.addWidget(self.size_box)
        size_box_layout.setSpacing(0)

        spinbox_layout = QVBoxLayout()
        spinbox_layout.addLayout(size_box_layout)
        spinbox_layout.setAlignment(Qt.AlignLeft)

        checkbox_layout = QVBoxLayout()
        self.open_checkbox = QCheckBox('Open Upon Resize')
        checkbox_layout.addWidget(self.open_checkbox)
        checkbox_layout.setAlignment(Qt.AlignLeft)

        parameters_layout = QHBoxLayout()
        parameters_layout.addLayout(spinbox_layout)
        parameters_layout.addLayout(checkbox_layout)

        parameters_group.setLayout(parameters_layout)

        layout.addWidget(resize_group)
        layout.addWidget(parameters_group)
        layout.addLayout(button_layout)
        layout.addWidget(self.message, alignment=Qt.AlignCenter)
        layout.addStretch(1)

        self.setLayout(layout)

        self.tomb_path_button.clicked.connect(self.select_tomb_path)
        self.key_path_button.clicked.connect(self.select_key_path)
        self.resize_button.clicked.connect(self.resize_selected_tomb)

    def select_tomb_path(self):
        """Select the path of the tomb to open.

        If the tomb's key is in the same directory as the tomb and follows the
        pattern of file.tomb.key, then the key's path is filled in its text box.
        """
        filename, ok = QFileDialog.getOpenFileName(self, 'Tomb Container')

        if ok:
            self.tomb_path.setText(filename)

            key = "{}.key" .format(self.tomb_path.text())

            if os.path.isfile(key):
                self.key_path.setText(key)

    def select_key_path(self):
        """Select the path of the key to open."""
        filename, ok = QFileDialog.getOpenFileName(self, 'Tomb Key')

        if ok:
            self.key_path.setText(filename)

    def resize_selected_tomb(self):
        """Resize the selected tomb with the selected key, key password, and sudo password.

        The key's password and sudo password are not stored as strings so that the only
        place passwords are stored is in QLineEdit. QLineEdit will clear the passwords,
        however we must make sure that the application is not stored in swap.
        """
        resize_command = wrapper.resize_tomb(self.tomb_path.text(),
                                             self.size_box.value(),
                                             self.key_path.text(),
                                             self.key_password.text(),
                                             self.path,
                                             sudo=self.sudo_password.text())
        if resize_command[0] is not None:
            self.message.setText('Tomb Resized Successfully')

            if self.open_checkbox.isChecked():
                    open_command = wrapper.open_tomb(self.tomb_path.text(),
                                                     self.key_path.text(),
                                                     self.key_password.text(),
                                                     self.path,
                                                     sudo=self.sudo_password.text(),
                                                     debug=self.debug)

                    if open_command[0] is not None:
                        self.message.setText('Tomb Opened Successfully')

            self.tomb_path.clear()
            self.key_path.clear()
            self.key_password.clear()
            self.sudo_password.clear()


class AdvancedTomb(QWidget):
    """Creates the abstract widget to be used as the advanced page."""

    def __init__(self, path, parent=None):
        """Initialize the advanced page's configuration group."""
        super(AdvancedTomb, self).__init__(parent)

        self.path = path

        layout = QVBoxLayout()

        advanced_group = QGroupBox('Advanced Tomb Operations')

        self.key_path = QLineEdit()
        self.key_path_button = QPushButton('Select Path')
        key_path_layout = QHBoxLayout()
        key_path_layout.addWidget(self.key_path)
        key_path_layout.addWidget(self.key_path_button)

        self.image_path = QLineEdit()
        self.image_path_button = QPushButton('Select Path')
        image_path_layout = QHBoxLayout()
        image_path_layout.addWidget(self.image_path)
        image_path_layout.addWidget(self.image_path_button)

        self.key_password = QLineEdit()
        self.key_password.setEchoMode(QLineEdit.Password)

        advanced_layout = QFormLayout()
        advanced_layout.addRow('Key Path:', key_path_layout)
        advanced_layout.addRow('Image Path:', image_path_layout)
        advanced_layout.addRow('Key Password:', self.key_password)
        advanced_group.setLayout(advanced_layout)

        self.engrave_button = QPushButton('Engrave Tomb')
        self.engrave_button.setFixedWidth(200)
        self.bury_button = QPushButton('Bury Tomb')
        self.bury_button.setFixedWidth(200)
        self.exhume_button = QPushButton('Exhume Tomb')
        self.exhume_button.setFixedWidth(200)

        button_layout = QVBoxLayout()
        button_layout.addWidget(self.engrave_button, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.bury_button, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.exhume_button, alignment=Qt.AlignCenter)
        button_layout.setContentsMargins(25, 25, 25, 25)

        self.message = QLabel()

        layout.addWidget(advanced_group)
        layout.addLayout(button_layout)
        layout.addWidget(self.message, alignment=Qt.AlignCenter)
        layout.addStretch(1)

        self.setLayout(layout)

        self.key_path_button.clicked.connect(self.select_key_path)
        self.image_path_button.clicked.connect(self.select_image_path)
        self.engrave_button.clicked.connect(self.engrave_selected_key)
        self.bury_button.clicked.connect(self.bury_selected_key)
        self.exhume_button.clicked.connect(self.exhume_selected_key)

    def select_key_path(self):
        """Select the path of the key to open."""
        filename, ok = QFileDialog.getOpenFileName(self, 'Tomb Key')

        if ok:
            self.key_path.setText(filename)

    def select_image_path(self):
        """Select the path of the image to open."""
        filename, ok = QFileDialog.getOpenFileName(self, 'Image')

        if ok:
            self.image_path.setText(filename)

    def engrave_selected_key(self):
        """Engrave the selected key into a QR png using QREncode."""
        engrave_command = wrapper.engrave_tomb(self.key_path.text())

        if engrave_command is not None:
            self.message.setText('Key Engraved Successfully')
            self.key_path.clear()

    def bury_selected_key(self):
        """Bury the selected key inside the given image using Steghide."""
        bury_command = wrapper.bury_tomb(self.image_path.text(),
                                         self.key_path.text(),
                                         self.key_password.text())

        if bury_command is not None:
            self.message.setText('Key Buried Successfully')
            self.key_path.clear()
            self.image_path.clear()
            self.key_password.clear()

    def exhume_selected_key(self):
        """Retrieve a buried key from the given image using Steghide."""
        exhume_command = wrapper.exhume_tomb(self.image_path.text(), self.key_password.text())

        if exhume_command is not None:
            self.message.setText('Key Exhumed Successfully')
            self.image_path.clear()
            self.key_password.clear()


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
    sudo_state_changed = pyqtSignal(bool)
    swap_state_changed = pyqtSignal(bool)
    tomb_path_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        """Initialize the config page's configuration group."""
        super(ConfigTomb, self).__init__(parent)

        config_directory = AppDirs('mausoleum', 'Mandeep').user_config_dir

        if not os.path.exists(config_directory):
            os.makedirs(config_directory)

        settings = importlib.resources.files(__package__) / 'settings.toml'
        with open(settings) as default_config:
            default_config = default_config.read()

        self.user_config_file = os.path.join(config_directory, 'settings.toml')
        if not os.path.isfile(self.user_config_file) or os.stat(self.user_config_file).st_size == 0:
            with open(self.user_config_file, 'a') as new_config_file:
                new_config_file.write(default_config)

        with open(self.user_config_file) as conffile:
            self.config = pytoml.load(conffile)

        config_box = QGroupBox("Configure Mausoleum")

        self.tomb_path_label = QLabel('Tomb Path', self)
        self.tomb_path_line = QLineEdit()
        self.tomb_path_line.setReadOnly(True)
        self.tomb_path_button = QPushButton('Select Path')

        self.tomb_path_button.clicked.connect(self.select_tomb_install_path)

        tomb_path_layout = QVBoxLayout()

        tomb_path_config_layout = QHBoxLayout()
        tomb_path_config_layout.addWidget(self.tomb_path_label)
        tomb_path_config_layout.addWidget(self.tomb_path_line)
        tomb_path_config_layout.addWidget(self.tomb_path_button)

        self.sudo_checkbox = QCheckBox('Enable Sudo Password')
        self.ignore_swap_checkbox = QCheckBox('Ignore Swap Partition')
        options_layout = QHBoxLayout()
        options_layout.addWidget(self.sudo_checkbox)
        options_layout.addWidget(self.ignore_swap_checkbox)

        self.sudo_checkbox.setChecked(self.config['configuration'].get('sudo_allowed_in_gui', True))
        self.sudo_checkbox.stateChanged.connect(self.emit_sudo_state)

        self.ignore_swap_checkbox.stateChanged.connect(self.emit_swap_state)

        tomb_path_layout.addLayout(tomb_path_config_layout)

        tomb_path_layout.addLayout(options_layout)
        config_box.setLayout(tomb_path_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(config_box)
        main_layout.addStretch(1)
        self.setLayout(main_layout)

        self.set_tomb_path(self.config)

    def select_tomb_install_path(self):
        """Select Tomb's installation path."""
        tomb_install_path = QFileDialog.getExistingDirectory(
                            self, 'Select Tomb Installation Path')

        if tomb_install_path and os.path.isfile(tomb_install_path):
            self.tomb_path_line.setText(tomb_install_path)

            self.config['configuration']['path'] = tomb_install_path

            with open(self.user_config_file, 'w') as config_file:
                pytoml.dump(self.config, config_file)

            self.tomb_path_changed.emit(tomb_install_path)

    def set_tomb_path(self, config):
        """Set Tomb's current installation path."""
        current_tomb_path = config['configuration']['path']
        if os.path.isdir(current_tomb_path):
            self.tomb_path_line.setText(current_tomb_path)
        else:
            self.tomb_path_line.setText(shutil.which('tomb'))

    def emit_sudo_state(self):
        """Emit a signal to change all pages that use a Sudo Password."""
        self.sudo_state_changed.emit(self.sudo_checkbox.isChecked())

    def emit_swap_state(self):
        """Emit a signal to ignore the swap partition when opening a tomb."""
        self.swap_state_changed.emit(self.ignore_swap_checkbox.isChecked())


class Mausoleum(QDialog):
    """Creates the main window that stores all of the widgets necessary for the application."""

    def __init__(self, parent=None):
        """Initialize the window size and title and instantiate the tab widget pages."""
        super(Mausoleum, self).__init__(parent)
        self.resize(600, 600)
        self.setWindowTitle('Mausoleum')
        window_icon = importlib.resources.files('mausoleum.images') / 'ic_vpn_key_black_48dp_1x.png'
        self.setWindowIcon(QIcon(str(window_icon)))

        self.config_page = ConfigTomb()
        self.tomb_current_path = self.config_page.tomb_path_line.text()

        self.create_page = CreateTomb(self.tomb_current_path)
        self.open_page = OpenTomb(self.tomb_current_path)
        self.close_page = CloseTomb(self.tomb_current_path)
        self.resize_page = ResizeTomb(self.tomb_current_path)
        self.list_page = ListTomb(self.tomb_current_path)
        self.advanced_page = AdvancedTomb(self.tomb_current_path)

        self.pages = QTabWidget()
        self.pages.addTab(self.create_page, 'Create')
        self.pages.addTab(self.open_page, 'Open')
        self.pages.addTab(self.close_page, 'Close')
        self.pages.addTab(self.resize_page, 'Resize')
        self.pages.addTab(self.list_page, 'List')
        self.pages.addTab(self.advanced_page, 'Advanced')
        self.pages.addTab(self.config_page, 'Config')

        dialog_layout = QHBoxLayout()
        dialog_layout.addWidget(self.pages)

        self.setLayout(dialog_layout)

        self.update_settings()

        self.create_page.create_button.clicked.connect(self.update_list_items)
        self.open_page.open_button.clicked.connect(self.update_list_items)
        self.close_page.close_all_button.clicked.connect(self.update_list_items)
        self.close_page.force_close_button.clicked.connect(self.update_list_items)
        self.resize_page.resize_button.clicked.connect(self.update_list_items)
        self.config_page.sudo_state_changed.connect(self.update_sudo)
        self.config_page.swap_state_changed.connect(self.update_swap)
        self.config_page.tomb_path_changed.connect(self.update_tomb_path)

    def update_list_items(self):
        """Update the list of active tombs whenever a tomb is opened or closed."""
        QTimer.singleShot(2000, self.list_page.update_list_items)

    def update_settings(self):
        """Update the GUI settings based on what the user has defined in the config.

        At startup, the user's preferences will be set in the GUI. Any time there is
        a new option added to the config page, it should be added here.
        """
        self.update_sudo(self.config_page.sudo_checkbox.checkState())

    def update_sudo(self, state):
        """Set the visibility of the Sudo Password QLineEdit based on the config settings.

        In Qt6, setRowVisible(bool) was added. However, since it wasn't backported to Qt5,
        we have to use addRow and removeRow to achieve the same outcome.
        """
        if state:
            if self.create_page.tomb_layout.rowCount() == 4:
                sudo_password = QLineEdit()
                sudo_password.setEchoMode(QLineEdit.Password)
                self.create_page.sudo_password = sudo_password
                self.create_page.tomb_layout.addRow('Sudo Password:', sudo_password)

            if self.open_page.open_layout.rowCount() == 3:
                sudo_password = QLineEdit()
                sudo_password.setEchoMode(QLineEdit.Password)
                self.open_page.sudo_password = sudo_password
                self.open_page.open_layout.addRow('Sudo Password:', sudo_password)

            if self.resize_page.resize_layout.rowCount() == 3:
                sudo_password = QLineEdit()
                sudo_password.setEchoMode(QLineEdit.Password)
                self.resize_page.sudo_password = sudo_password
                self.resize_page.resize_layout.addRow('Sudo Password:', sudo_password)

            self.config_page.config['configuration']['sudo_allowed_in_gui'] = True

            with open(self.config_page.user_config_file, 'w') as config_file:
                pytoml.dump(self.config_page.config, config_file)
        else:
            if self.create_page.tomb_layout.rowCount() == 5:
                self.create_page.tomb_layout.removeRow(4)
            if self.open_page.open_layout.rowCount() == 4:
                self.open_page.open_layout.removeRow(3)
            if self.resize_page.resize_layout.rowCount() == 4:
                self.resize_page.resize_layout.removeRow(3)

            self.config_page.config['configuration']['sudo_allowed_in_gui'] = False

            with open(self.config_page.user_config_file, 'w') as config_file:
                pytoml.dump(self.config_page.config, config_file)

    def update_swap(self, state):
        """Update the debug flag on relevant pages so that swap partitions are ignored."""
        if state:
            self.create_page.debug = True
            self.open_page.debug = True
            self.resize_page.debug = True
        else:
            self.create_page.debug = False
            self.open_page.debug = False
            self.resize_page.debug = False

    def update_tomb_path(self, new_path):
        """Use the new tomb path that the user submits."""

        self.tomb_current_path = new_path

        self.create_page.path = new_path
        self.open_page.path = new_path
        self.close_page.path = new_path
        self.resize_page.path = new_path
        self.list_page.path = new_path
        self.advanced_page.path = new_path


def main():
    application = QApplication(sys.argv)
    window = Mausoleum()
    desktop = QDesktopWidget().availableGeometry()
    width = (desktop.width() - window.width()) / 2
    height = (desktop.height() - window.height()) / 2
    window.show()
    window.move(int(width), int(height))
    sys.exit(application.exec_())


if __name__ == "__main__":
    main()
