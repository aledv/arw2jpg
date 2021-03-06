from setuptools import setup

def get_requires():
    reqs = []
    for line in open('requirements.txt', 'r').readlines():
        reqs.append(line)
    return reqs

setup(
    name = 'arw2jpg',
    version = '1.0',
    description = 'Commandline utility to convert raw files to jpg',
    author = 'aledv, devincody',
    author_email = '',
    install_requires=get_requires(),
    packages = ['arw2jpg'],
    entry_points={
        'console_scripts': ['arw2jpg = arw2jpg.arw2jpg:main'],
    }
)