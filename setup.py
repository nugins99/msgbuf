from setuptools import setup, find_packages

#package_data={'msgbuf': ['templates/hpp.template']},

setup(
    name='msgbuf',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    package_data={'msgbuf': ['templates/*']},
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
