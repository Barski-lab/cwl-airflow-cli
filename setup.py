from setuptools import setup, find_packages
import os

setup(
    name='airflow-cwl-cli',
    description='Python package to add and check status of the submitted to Airflow jobs',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    version='0.0.1',
    url='https://github.com/Barski-lab/airflow_cwl_cli',
    download_url=('https://github.com/Barski-lab/airflow_cwl_cli'),
    author='Michael Kotliar',
    author_email='misha.kotliar@gmail.com',
    license = 'MIT',
    packages=find_packages(),
    install_requires=[
        'MySQL-python>=1.2.5',
        'ConfigParser>=3.5.0, <3.6.0',
        'uuid==1.30',
        'ruamel.yaml<0.15'
    ],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            "airflow-cwl-cli=cli.main:main"
        ]
    }
)