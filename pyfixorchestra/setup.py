import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="library",
    version="1.0.0",
    author="Nathanael Judge",
    author_email="nzjudge@mtu.edu",
    description="A python package to create a FIX dictionary",
    long_description=long_description,
    url="https://github.com/chillaranand/library",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
