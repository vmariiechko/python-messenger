from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="python-messenger-marik348",
    version="1.2.0",
    author="Vadym Mariiechko",
    author_email="vadimich348@gmail.com",
    description="Client/server single chat messenger",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marik348/python-messegner",
    packages=find_packages(),
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8, <4',
    keywords="messenger, chat",
)
