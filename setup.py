from setuptools import setup, find_packages

setup(
    name='WinningEdge',
    version='1.0.0',
    packages=find_packages(),  # Automatically discover and include all packages
    install_requires=[
        # List your package dependencies here
        'numpy',
        'pandas'
    ],
    entry_points={
        'console_scripts': [
            # Define any command-line scripts here
            'your_script = your_package.module:main_function',
        ],
    },
    author='Peter Sushko',
    author_email='psushko@uw.edu',
    description='Poker Optimization Tool for Heads Up Texas HoldEm',
    url='https://github.com/WinningEdge-AI/WinningEdge',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License ::  MIT License',
      
    ],
)