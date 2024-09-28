from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='stockstreamdb',
    version='1.0.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=required,
    entry_points={
        'console_scripts': [
            'stockstreamdb=interfaces.cli.cli:main',
        ],
    },
    python_requires='>=3.6',
)
