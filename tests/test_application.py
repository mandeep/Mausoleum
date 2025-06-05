import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog
import pytest

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
    window.create_page.debug = True
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
    window.open_page.debug = True
    button = window.open_page.open_button
    qtbot.mouseClick(button, Qt.LeftButton)
    assert window.open_page.message.text() == 'Tomb Opened Successfully'


def test_open_dialog(window, qtbot, monkeypatch):
    """Test the Set Tomb Path dialog on the Open page."""
    button = window.open_page.tomb_path_button
    
    def fake_get_open_file_name(*args, **kwargs):
        return ("/path/to/test/tomb", "All Files (*.*)")
    
    monkeypatch.setattr(QFileDialog, "getOpenFileName", fake_get_open_file_name)

    qtbot.mouseClick(button, Qt.LeftButton)

    assert window.open_page.tomb_path.text() == "/path/to/test/tomb"


def test_resize_dialog(window, qtbot, monkeypatch):
    """Test the Set Tomb Path dialog on the Resize page."""
    button = window.resize_page.tomb_path_button
    
    def fake_get_open_file_name(*args, **kwargs):
        return ("/path/to/test/tomb", "All Files (*.*)")
    
    monkeypatch.setattr(QFileDialog, "getOpenFileName", fake_get_open_file_name)

    qtbot.mouseClick(button, Qt.LeftButton)

    assert window.resize_page.tomb_path.text() == "/path/to/test/tomb"


def test_open_key_path(window, qtbot, monkeypatch):
    """Test the Select Key dialog on the Open page."""
    button = window.open_page.key_path_button
    
    def fake_get_open_file_name(*args, **kwargs):
        return ("/path/to/test/test.tomb.key", "All Files (*.*)")
    
    monkeypatch.setattr(QFileDialog, "getOpenFileName", fake_get_open_file_name)

    qtbot.mouseClick(button, Qt.LeftButton)

    assert window.open_page.key_path.text() == "/path/to/test/test.tomb.key"


def test_resize_key_path(window, qtbot, monkeypatch):
    """Test the Select Key dialog on the Resize page."""
    button = window.resize_page.key_path_button
    
    def fake_get_open_file_name(*args, **kwargs):
        return ("/path/to/test/test.tomb.key", "All Files (*.*)")
    
    monkeypatch.setattr(QFileDialog, "getOpenFileName", fake_get_open_file_name)

    qtbot.mouseClick(button, Qt.LeftButton)

    assert window.resize_page.key_path.text() == "/path/to/test/test.tomb.key"


def test_list_items(window, qtbot, monkeypatch):
    """Test the Update List Items on the List page."""
    button = window.list_page.update_list_button
    qtbot.mouseClick(button, Qt.LeftButton)


def test_advanced_key_path(window, qtbot, monkeypatch):
    """Test the Select Key dialog on the Advanced page."""
    button = window.advanced_page.key_path_button
    
    def fake_get_open_file_name(*args, **kwargs):
        return ("/path/to/test/test.tomb.key", "All Files (*.*)")
    
    monkeypatch.setattr(QFileDialog, "getOpenFileName", fake_get_open_file_name)

    qtbot.mouseClick(button, Qt.LeftButton)

    assert window.advanced_page.key_path.text() == "/path/to/test/test.tomb.key"


def test_image_path(window, qtbot, monkeypatch):
    """Test the Select Image dialog on the Advanced page."""
    button = window.advanced_page.image_path_button
    
    def fake_get_open_file_name(*args, **kwargs):
        return ("/path/to/test/test.jpg", "All Files (*.*)")
    
    monkeypatch.setattr(QFileDialog, "getOpenFileName", fake_get_open_file_name)

    qtbot.mouseClick(button, Qt.LeftButton)

    assert window.advanced_page.image_path.text() == "/path/to/test/test.jpg"


def test_install_path(window, qtbot, monkeypatch, tmp_path):
    """Test the Tomb Install Path dialog on the Config page."""
    fake_file = tmp_path / 'tomb'
    fake_file.write_text("fake binary content")

    widget = window.config_page

    # Monkeypatch QFileDialog to return the directory containing the fake file
    monkeypatch.setattr(QFileDialog, "getExistingDirectory", lambda *args, **kwargs: str(tmp_path))

    # Monkeypatch os.path.isfile to simulate the expected file check
    monkeypatch.setattr(os.path, "isfile", lambda path: path == str(tmp_path))

    # Optionally, monkeypatch config writing if needed
    monkeypatch.setattr(widget, "user_config_file", tmp_path / "config.toml")

    # Spy on signal (optional)
    with qtbot.waitSignal(widget.tomb_path_changed, timeout=1000) as blocker:
        widget.select_tomb_install_path()

    assert widget.tomb_path_line.text() == str(tmp_path)
    assert blocker.args == [str(tmp_path)]


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
    window.resize_page.open_checkbox.setChecked(True)
    window.resize_page.debug = True
    button = window.resize_page.resize_button
    qtbot.mouseClick(button, Qt.LeftButton)


def test_close_page_force_close_resize(window, qtbot):
    """Test the Force Close Tombs on the Close tab."""
    window.pages.setCurrentIndex(2)
    button = window.close_page.force_close_button
    qtbot.mouseClick(button, Qt.LeftButton)


def test_sudo_checkbox(window):
    """Test that the sudo checkbox correctly adds/removes the sudo lineedit."""
    window.config_page.sudo_checkbox.setChecked(False)
    assert window.create_page.tomb_layout.rowCount() == 4
    assert window.open_page.open_layout.rowCount() == 3
    assert window.resize_page.resize_layout.rowCount() == 3

    window.config_page.sudo_checkbox.setChecked(True)
    assert window.create_page.tomb_layout.rowCount() == 5
    assert window.open_page.open_layout.rowCount() == 4
    assert window.resize_page.resize_layout.rowCount() == 4


def test_swap_checkbox(window):
    """Test that the ignore swap checkbox correctly sets the debug flag on pages."""
    window.config_page.ignore_swap_checkbox.setChecked(True)
    assert window.create_page.debug is True
    assert window.open_page.debug is True
    assert window.resize_page.debug is True

    window.config_page.ignore_swap_checkbox.setChecked(False)
    assert window.create_page.debug is False
    assert window.open_page.debug is False
    assert window.resize_page.debug is False


def test_engrave_key(window, qtbot, key):
    """Test engraving the key inside a QR image."""
    window.pages.setCurrentIndex(5)
    window.advanced_page.key_path.setText(key)
    button = window.advanced_page.engrave_button
    qtbot.mouseClick(button, Qt.LeftButton)


def test_exhume_bury_key(window, qtbot, key, image_file, password):
    """Test burying the key inside the given image file."""
    window.pages.setCurrentIndex(5)
    window.advanced_page.key_path.setText(key)
    window.advanced_page.image_path.setText(image_file)
    window.advanced_page.key_password.setText(password)
    button = window.advanced_page.bury_button
    qtbot.mouseClick(button, Qt.LeftButton)

    window.pages.setCurrentIndex(5)
    window.advanced_page.image_path.setText(image_file)
    window.advanced_page.key_password.setText(password)
    button = window.advanced_page.exhume_button
    qtbot.mouseClick(button, Qt.LeftButton)
