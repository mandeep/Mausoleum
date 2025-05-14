##########
Change Log
##########

All notable changes to this project will be documented in this file.

Unreleased
==========

0.11.0 - 2024-07-28
===================

- Add a setting in the GUI Config Page that allows the user to control whether or not sudo can be entered in the GUI
  This setting is currently set to True by default, which is the standard behavior. In the future this setting will be set
  to False and the user will need to enter the sudo password in the terminal

0.10.3 - 2024-05-28
===================

-  Fix issue with importlib referencing the filename of mausoleum instead of the package name

0.10.2 - 2024-05-20
===================

-  Fix issue with Random Integer Key option where the tomb would not be created. This was due to a change in the Tomb API

0.10.1 - 2024-05-16
===================

-  Fix readability issue with README and PyPI

0.10.0 - 2024-05-15
===================

-  Migrate pkg_resources to importlib.resources for Python 3.12 support

0.9.0 - 2022-10-18
==================

-  Add missing commands leave and list
-  Add mountpoint support to enter command
-  Miscellaneous UI changes

-  Thanks to @djmattyg007 for massive help with this

0.8.7 - 2018-09-30
==================

-  Run tests in a temporary directory so that artifacts aren't left in the current working directory

0.8.6 - 2018-03-03
==================

-  Bring project out of maintenance mode and use Tomb 2.5

0.8.5 - 2017-11-27
==================

-  Move project into maintenance mode

0.8.4 - 2017-07-25
==================

-  Moved tests directory from the package directory to the project root directory

0.8.3 - 2017-06-07
==================

-  Replaced Codacity with Scrutinizer

0.8.2 - 2017-03-22
==================

GUI
---

Fixes
~~~~~

-  Fixed issue with changelog not rendering properly

0.8.1 - 2017-03-22
==================

GUI
---

Additions
~~~~~~~~~

-  New screenshot showcasing Advanced tab

0.8.0 - 2017-03-07
==================

GUI
---

Additions
~~~~~~~~~

-  Ability to engrave tomb key inside QR code
-  Ability to bury tomb key inside an existing image file
-  Ability to exhume tomb key from an existing image file

0.7.0 - 2017-02-18
==================

CLI
---

Additions
~~~~~~~~~

-  Ability to engrave tomb key inside QR code via command line
-  Ability to bury tomb key inside an existing image file via command line
-  Ability to exhume tomb key from an existing image file via command line

0.6.0 - 2017-02-18
==================

Wrapper
-------

Additions
~~~~~~~~~

-  Ability to engrave tomb key inside QR code
-  Ability to bury tomb key inside an existing image file
-  Ability to exhume tomb key from an existing image file

0.5.1 - 2017-02-17
==================

GUI
---

Changes
~~~~~~~

-  New GUI screenshot
-  Updated README with information regarding resizing of tombs

0.5.0 - 2017-02-16
==================

GUI
---

Additions
~~~~~~~~~

-  Ability to resize tombs

0.4.2 - 2016-12-31
==================

GUI
---

Additions
~~~~~~~~~

-  Key path automatically filled if found when opening tomb

0.4.1 - 2016-12-30
==================

Wrapper
-------

Additions
~~~~~~~~~

-  KDF iterations in forge_tomb function

GUI
---

Fixes
~~~~~

-  KDF iterations now working

0.4.0 - 2016-12-30
==================

Wrapper
-------

Additions
~~~~~~~~~

-  Read only keyword argument to use with open_tomb function

GUI
---

Additions
~~~~~~~~~

-  Ability to open Tombs in read only mode

0.3.3 - 2016-11-23
==================

Wrapper
-------

Additions
~~~~~~~~~

-  New function construct_tomb that digs, forges, and locks a new tomb container

0.3.2 - 2016-11-10
==================

GUI
---

Fixes
~~~~~

-  Settings.toml file now recognized

0.3.1 - 2016-11-10
==================

GUI
---

Additions
~~~~~~~~~

-  Warning message if Tomb installation not found

0.3.0 - 2016-11-09
==================

GUI
---

Additions
~~~~~~~~~

-  Config Tab with user configurable options
-  Tomb installation path option

Wrapper
-------

Additions
~~~~~~~~~

-  Tomb path argument in wrapper functions

0.2.6 - 2016-10-29
==================

GUI
---

Additions
~~~~~~~~~

-  Messages when tombs created or opened successfully

0.2.5 - 2016-10-28
==================

CLI
---

Additions
~~~~~~~~~

-  Docstring regarding key name formatting

0.2.4 - 2016-10-26
==================

GUI
---

Additions
~~~~~~~~~~

-  Settings.toml file for user configuration

0.2.3 - 2016-10-19
==================

GUI
---

Additions
~~~~~~~~~

-  Clear all text boxes upon creation and opening of tombs

Wrapper
-------

Additions
~~~~~~~~~

-  List all tombs function

0.2.2 - 2016-10-18
==================

GUI
---

Additions
~~~~~~~~~

-  Checkbox for KDF iterations
-  Confirmation text box for key password

Wrapper
-------

Additions
~~~~~~~~~

-  Ability to slam tombs


0.2.1 - 2016-10-17
==================

GUI
---

Additions
~~~~~~~~~

-  Renamed urandom key generation to Random Integer Key

0.2.0 - 2016-10-16
===================

GUI
---

Additions
~~~~~~~~~

-  Checkbox for urandom key generation

Wrapper
-------

Additions
~~~~~~~~~

-  Ability to close all tombs

0.1.0 - 2016-10-11
===================

-  Created CLI, GUI, and wrappers for Tomb
