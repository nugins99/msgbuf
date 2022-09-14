from setuptools import setup, find_packages

setup(
    name='msgbuf',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'Jinja2',
        'MarkupSafe',
        'PyYAML'
    ],
    entry_points={
        'console_scripts': [
            'msgbufc = msgbuf.main:main'
        ] 
    }
)
