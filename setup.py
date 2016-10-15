from setuptools import setup


setup(
    name='Mausoleum',
    version='0.0.1',
    description="A Python wrapper for Tomb",
    author="Mandeep",
    author_email='info@mandeep.xyz',
    url='https://github.com/mandeep/Mausoleum',
    packages=['mausoleum', 'mausoleum.images',
              'mausoleum.tests'],
    package_data={'mausoleum.images': ['*.png']},
    entry_points={
        'console_scripts': [
            'mausoleum-gui=mausoleum.application:main',
            'mausoleum=mausoleum.wrapper:cli'
        ]
    },
    install_requires=[
        'click',
        'pyqt5'
    ],
    keywords='Mausoleum',
    classifiers=[
        'Programming Language :: Python :: 3.5',
    ]
)
