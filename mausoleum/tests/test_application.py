import pkg_resources

import pytest

from PyQt5.QtCore import Qt

from mausoleum import application


@pytest.fixture
def window(qtbot):
    """Create an instance of Mausoleum to pass to test functions.

    window is used as a pytest fixture that allows passing it to test functions. Qtbot
    uses qApp to open a new main window for each test function.
    """
    new_window = application.Mausoleum()
    qtbot.add_widget(new_window)
    new_window.show()
    yield new_window


@pytest.fixture
def name():
    """Use test1.tomb as the tomb name to pass to test functions."""
    return 'test1.tomb'


@pytest.fixture
def key():
    """Use test1.tomb.key as the tomb key name to pass to test functions."""
    return 'test1.tomb.key'


@pytest.fixture
def password():
    """Use test_password as the tomb password to pass to test functions."""
    return 'test_password'


@pytest.fixture
def image_file():
    """Pass a JPEG file resource as an argument to the unit tests."""
    file = pkg_resources.resource_filename('mausoleum.tests', 'test.jpg')
    return file


def test_window_title(window):
    """Check the window title of the main window."""
    assert window.windowTitle() == 'Mausoleum'


def test_create_page_failure(window, qtbot):
    """Test tomb creation with key passwords that don't match."""
    button = window.create_page.create_button
    window.create_page.key_password.setText('1')
    window.create_page.confirm_password.setText('2')
    qtbot.mouseClick(button, Qt.LeftButton)
    assert window.create_page.message.text() == 'Key Passwords Do Not Match'


def test_create_page(window, qtbot, name, key, password):
    """Test tomb creation and tomb opening."""
    window.create_page.tomb_name.setText(name)
    window.create_page.key_name.setText(key)
    window.create_page.key_password.setText(password)
    window.create_page.confirm_password.setText(password)
    window.create_page.random_checkbox.setChecked(True)
    window.create_page.open_checkbox.setChecked(True)
    button = window.create_page.create_button
    qtbot.mouseClick(button, Qt.LeftButton)
    assert window.create_page.message.text() == 'Tomb Opened Successfully'


def test_close_page_close(window, qtbot):
    """Test the Close All Tombs button on the Close tab."""
    window.pages.setCurrentIndex(2)
    button = window.close_page.close_all_button
    qtbot.mouseClick(button, Qt.LeftButton)


def test_open_page(window, qtbot, name, key, password):
    """Test tomb opening on the Open tab."""
    window.pages.setCurrentIndex(1)
    window.open_page.tomb_path.setText(name)
    window.open_page.key_path.setText(key)
    window.open_page.key_password.setText(password)
    button = window.open_page.open_button
    qtbot.mouseClick(button, Qt.LeftButton)
    assert window.open_page.message.text() == 'Tomb Opened Successfully'


def test_close_page_force_close(window, qtbot):
    """Test the Force Close Tombs on the Close tab."""
    window.pages.setCurrentIndex(2)
    button = window.close_page.force_close_button
    qtbot.mouseClick(button, Qt.LeftButton)


def test_resize_page(window, qtbot, name, key, password):
    """Test tomb resizing on the Resize tab."""
    window.pages.setCurrentIndex(3)
    window.resize_page.tomb_path.setText(name)
    window.resize_page.key_path.setText(key)
    window.resize_page.key_password.setText(password)
    window.resize_page.size_box.setValue(50)
    button = window.resize_page.resize_button
    qtbot.mouseClick(button, Qt.LeftButton)


def test_engrave_key(window, qtbot, key):
    """Test engraving the key inside a QR image."""
    window.pages.setCurrentIndex(5)
    window.advanced_page.key_path.setText(key)
    button = window.advanced_page.engrave_button
    qtbot.mouseClick(button, Qt.LeftButton)


def test_bury_key(window, qtbot, key, image_file, password):
    """Test burying the key inside the given image file."""
    window.pages.setCurrentIndex(5)
    window.advanced_page.key_path.setText(key)
    window.advanced_page.image_path.setText(image_file)
    window.advanced_page.key_password.setText(password)
    button = window.advanced_page.bury_button
    qtbot.mouseClick(button, Qt.LeftButton)


def exhume_bury_key(window, qtbot, image_file, password):
    """Test exhuming the key from inside the given image file."""
    window.pages.setCurrentIndex(5)
    window.advanced_page.image_path.setText(image_file)
    window.advanced_page.key_password.setText(password)
    button = window.advanced_page.exhume_button
    qtbot.mouseClick(button, Qt.LeftButton)
