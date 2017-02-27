from setuptools import setup, find_packages

setup(
    name='poobrains-markdown',
    description='markdown extension for poobrains',
    author='phryk',
    install_requires=['poobrains', 'markdown'],
    extras_require={
        'dev': ['pudb'], 
    },
    packages=find_packages(),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 2.7',
    ]
)
