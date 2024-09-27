from setuptools import setup, find_packages

setup(
    name='stockstreamdb',
    version='1.0.0',
    packages=['interfaces', 'interfaces.cli'],
    package_dir={'': 'src'},
    install_requires=[
        # Your dependencies
    ],
    entry_points={
        'console_scripts': [
            'stockstreamdb=interfaces.cli.cli:main',
        ],
    },
    python_requires='>=3.6',
)
