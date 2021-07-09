from setuptools import setup

setup(
    name='tasktimer',
    version='',
    packages=['tasktimer'],
    url='',
    license='',
    author='thedjaney',
    author_email='thedjaney@gmail.com',
    description='',
    entry_points={
        'console_scripts': ['tasktimer=tasktimer.cli:main'],
    },
    install_requires=[
        'requests~=2.25.1',
        'click~=8.0.1',
    ]
)
