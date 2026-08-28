"""
Setup script for c3ppc - C3++ to C compiler
"""

from setuptools import setup, find_packages

setup(
    name="c3ppc",
    version="0.1.0",
    description="C3++ to C compiler using PyLGEN",
    long_description=open("README.md").read() if __import__("os").path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    author="Roy Perry",
    author_email="roypery2010@gmail.com",
    url="https://github.com/c3pp-lang/c3ppc",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "pylgen-core>=0.6.0",
    ],
    entry_points={
        "console_scripts": [
            "c3ppc=c3ppc.compiler:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Compilers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="c3 c3pp compiler lexer parser pylgen",
)
