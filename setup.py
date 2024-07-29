# setup.py

from setuptools import setup, find_packages

setup(
    name="gheruq",
    version="0.1.1",
    packages=find_packages(),
    description="A package for root detection in Maltese",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Kellen Parker van Dam",
    author_email="patkaiist@gmail.com",
    url="https://github.com/patkaiist/gheruq",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
    ],
    python_requires=">=3.6",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "gheruq-cli=cli:main",
        ],
    },
)
