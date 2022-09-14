from setuptools import setup

setup(
    name='msgbuf',
    version='0.0.1',
    install_requires=[
        'Jinja2',
        'MarkupSafe',
        'PyYAML'
    ],
    entry_points={
        'console_scripts': [
            'msgbufc = msgbuf:main'
        ] 
    }
)
