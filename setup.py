from setuptools import setup, find_packages

setup(
    name='tasktimer',
    version='0.0.1',
    packages=find_packages(),
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
