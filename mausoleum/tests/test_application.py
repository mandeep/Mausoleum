import pytest

from PyQt5.QtCore import Qt

from mausoleum import application


@pytest.fixture
def window(qtbot):
    """Window is used as a pytest fixture that allows passing it to test functions. Qtbot
    uses qApp to open a new main window."""
    new_window = application.Mausoleum()
    qtbot.add_widget(new_window)
    new_window.show()
    return new_window


@pytest.fixture
def name():
    return 'test1.tomb'


@pytest.fixture
def key():
    return 'test1.tomb.key'


@pytest.fixture
def password():
    return 'test_password'


def test_window_title(window):
    assert window.windowTitle() == 'Mausoleum'


def test_create_page(window, qtbot, name, key, password):
    window.create_page.tomb_name.setText(name)
    window.create_page.key_name.setText(key)
    window.create_page.key_password.setText(password)
    window.create_page.urandom_checkbox.setChecked(True)
    button = window.create_page.create_button
    qtbot.mouseClick(button, Qt.LeftButton)


def test_open_page(window, qtbot, name, key, password):
    window.pages.setCurrentIndex(1)
    window.open_page.tomb_path.setText(name)
    window.open_page.key_path.setText(key)
    window.open_page.key_password.setText(password)
    button = window.open_page.open_button
    qtbot.mouseClick(button, Qt.LeftButton)


def test_close_page(window, qtbot):
    window.pages.setCurrentIndex(2)
    button = window.close_page.close_all_button
    qtbot.mouseClick(button, Qt.LeftButton)
