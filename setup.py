from setuptools import setup


setup(
    name='mausoleum',
    version='0.9.0',
    description='A Python GUI, CLI, and wrapper for Tomb',
    author='Mandeep',
    author_email='info@mandeep.xyz',
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
    keywords='Mausoleum',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
)
