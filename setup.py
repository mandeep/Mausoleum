from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'click'
]

test_requirements = [
    'pytest',
    'pytest-cov',
    'pytest-mock',
    'pytest-qt',
    'pytest-xvfb',

]

setup(
    name='Mausoleum',
    version='0.0.1',
    description="A GUI application for Tomb",
    long_description=readme,
    author="Mandeep",
    author_email='info@mandeep.xyz',
    url='https://github.com/mandeep/Mausoleum',
    packages=['mausoleum', 'mausoleum.images',
              'mausoleum.tests'],
    package_data={'mausoleum.images': ['*.png']},
    entry_points={
        'console_scripts': [
            'mausoleum=mausoleum.application:main',
            'erect=mausoleum.wrapper:cli'
        ]
    },
    install_requires=requirements,
    zip_safe=False,
    keywords='Mausoleum',
    classifiers=[
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
