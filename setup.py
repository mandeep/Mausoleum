from setuptools import setup


from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.rst").read_text()


setup(
    name='mausoleum',
    version='0.11.0',
    description='A Python GUI, CLI, and wrapper for Tomb',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    author='Mandeep',
    license='GPLv3+',
    url='https://github.com/mandeep/Mausoleum',
    packages=['mausoleum', 'mausoleum.images'],
    package_data={'mausoleum.images': ['*.png'], 'mausoleum': ['*.toml']},
    entry_points={
        'console_scripts': [
            'mausoleum-gui=mausoleum.application:main',
            'mausoleum=mausoleum.wrapper:cli'
        ]
    },
    install_requires=[
        'appdirs==1.4.3',
        'click==7.0',
        'pytoml==0.1.13',
    ],
    extras_require={'tests':
        ['pytest',
        'pytest-xvfb',
        'pytest-qt'
        ]
    },
    keywords='Mausoleum',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ]
)
