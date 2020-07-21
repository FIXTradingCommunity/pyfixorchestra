import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyfixorchestra",
    version="1.0.0",
    author="Nathanael Judge",
    author_email="nzjudge@mtu.edu",
    description="A python package to create a  python dictionary of FIX latest",
    long_description=long_description,
    url="https://github.com/FIXTradingCommunity/pyfixorchestra,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
