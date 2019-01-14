from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='thegoodtube',
    version='0.2.0',
    author="Mickaël Fontaine",
    description="REST API for youtube-dl",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.aravis-commerce.com/theGoodTube/api",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)
