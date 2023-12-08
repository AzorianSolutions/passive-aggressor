from setuptools import setup

setup(
    name='passive-aggressor',
    version='0.1.0',
    install_requires=[
        'click==8.1.3',
        'loguru==0.7.0',
    ],
    entry_points={
        'console_scripts': [
            'aggressor = app:cli',
        ],
    },
)
