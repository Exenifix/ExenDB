from setuptools import setup

with open('README.md') as readme_file:
    long_description = readme_file.read()

setup(
    name='exendb',
    version='0.0.1',
    author='Exenifix',
    license='MIT',
    url='https://github.com/Exenifix/ExenDB',
    description='A simple library that covers sqlite3\'s basic functionality.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=['exendb'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.7',
    package_dir={'': 'exendb'}
)