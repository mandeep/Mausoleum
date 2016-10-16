.. image:: mausoleum.png

|travis| |coveralls| |dependency| |codacy| |pypiversion| |pypistatus| |pythonversion| |pypiformat| |license|

Mausoleum consists of a command line application and GUI application wrapped around Tomb
(the Crypto Undertaker). Both applications were created with the intention of making
it easier for users to interact with Tomb.

.. image:: screenshot.png
    :align: center

************
Installation
************

As Mausoleum is purely a wrapper of Tomb, it requires Tomb to be installed locally. For Tomb installation
details, please see: https://www.dyne.org/software/tomb/. The Mausoleum GUI application requires PyQt5
to be installed locally. For PyQt5 installation instructions, please visit: https://www.riverbankcomputing.com/software/pyqt/download5.

With your environment set, the following command may be used to install Mausoleum::

    $  pip install mausoleum

If you would rather install from source, run::

    $  git clone https://github.com/mandeep/Mausoleum.git
    $  cd Mausoleum
    $  python setup.py install

*****
Usage
*****

To run the GUI application, simply run the following command in a terminal::

    $  mausoleum-gui


.. |travis| image:: https://img.shields.io/travis/mandeep/Mausoleum.svg 
    :target: https://travis-ci.org/mandeep/Mausoleum
.. |coveralls| image:: https://img.shields.io/coveralls/mandeep/Mausoleum.svg 
    :target: https://coveralls.io/github/mandeep/Mausoleum
.. |dependency| image:: https://img.shields.io/librariesio/github/mandeep/Mausoleum.svg
    :target: https://dependencyci.com/github/mandeep/Mausoleum
.. |codacy| image:: https://img.shields.io/codacy/grade/78a599f30d32444a98ba8a172edbed3d.svg 
    :target: https://www.codacy.com/app/bhutanimandeep/Mausoleum
.. |pypiversion| image:: https://img.shields.io/pypi/v/mausoleum.svg 
    :target: https://pypi.python.org/pypi/mausoleum/
.. |pypistatus| image:: https://img.shields.io/pypi/status/mausoleum.svg 
    :target: https://pypi.python.org/pypi/mausoleum/
.. |pythonversion| image:: https://img.shields.io/pypi/pyversions/mausoleum.svg 
    :target: https://pypi.python.org/pypi/mausoleum/
.. |pypiformat| image:: https://img.shields.io/pypi/format/mausoleum.svg
    :target: https://pypi.python.org/pypi/mausoleum/
.. |license| image:: https://img.shields.io/pypi/l/mausoleum.svg
    :target: https://pypi.python.org/pypi/mausoleum/