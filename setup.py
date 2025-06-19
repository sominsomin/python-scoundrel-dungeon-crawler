from setuptools import setup, find_packages

setup(
    name='scoundrel card game',
    version='1.0',
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    entry_points={
        'console_scripts': [
            'scoundrel=main:main',
        ],
    },
    description='A terminal-based card game',
    install_requires=['blessed'],
)