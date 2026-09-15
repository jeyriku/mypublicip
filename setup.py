from setuptools import setup, find_packages

setup(
    name='mypublicip',
    version='0.1.9',
    author='Jeremie Rouzet',
    author_email='jeremie.rouzet@netalps.fr',
    description='A module to retrieve the public IP address of the current connection.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/mypublicip',  # Replace with your actual URL
    packages=['mypublicip'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Replace with your actual license
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'pyvault-web>=1.1.1',
    ],
    entry_points={
        'console_scripts': [
            'mypublicip=mypublicip.cli:main',
        ],
    },
)
