from os import path
from setuptools import setup, find_packages

with open(path.join(path.dirname(__file__), "malt", "_version.py")) as f:
    version = f.readlines()[-1].split()[-1].strip("\"'")

requirements = [
    "gast"
]

classifiers = [
    "Natural Language :: English",
    "Intended Audience :: Developers",
    "Development Status :: 5 - Production/Stable",
    "License :: OSI Approved :: Apache Software License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3 :: Only",
]


description = {
    "maintainer": "Xanadu Inc.",
    "maintainer_email": "software@xanadu.ai",
    "url": "https://github.com/PennyLaneAI/diastatic-malt",
    "description": "A library for Python operator overloading",
    "long_description": open("README.md").read(),
    "long_description_content_type": "text/markdown",
    "license": "Apache License 2.0",
}


setup(
    name="diastatic-malt",
    provides=["malt"],
    packages=find_packages(include=["malt", "malt.*"]),
    version=version,
    python_requires=">=3.9",
    install_requires=requirements,
    classifiers=classifiers,
    **description,
)
