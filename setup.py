from setuptools import find_packages, setup

setup(
    name='ezmechmarket',
    version='1.0.6',
    packages=find_packages(),
    include_package_data=True,
    data_files = [('', ['praw.ini'])],
    zip_safe=False,
    install_requires=[
        'ezmechmarket',
    ],
)