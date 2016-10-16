from setuptools import setup


setup(
    name='mausoleum',
    version='0.0.1',
    description='A Python wrapper and GUI application for Tomb',
    author='Mandeep',
    author_email='info@mandeep.xyz',
    license='GPLv3+',
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
    ],
    keywords='Mausoleum',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ]
)
