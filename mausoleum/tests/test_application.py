import pytest

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QAction, QApplication, QDialog, QDesktopWidget, QFileDialog,
                             QGroupBox, QHBoxLayout, QLabel, QMainWindow, QMenuBar, QStatusBar,
                             QToolBar)

from mausoleum import application


@pytest.fixture
def window(qtbot):
    """Window is used as a pytest fixture that allows passing it to test functions. Qtbot
    uses qApp to open a new main window."""
    new_window = application.Mausoleum()
    qtbot.add_widget(new_window)
    new_window.show()
    return new_window


def test_window_title(window):
    assert window.windowTitle() == 'Mausoleum'


def test_create_page(window, qtbot):
    window.create_page.tomb_name.setText('test1.tomb')
    window.create_page.key_name.setText('test1.tomb.key')
    window.create_page.key_password.setText('test_password')
    button = window.create_page.create_button
    qtbot.mouseClick(button, Qt.LeftButton)
