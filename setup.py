from setuptools import setup, find_packages

setup(
    name="presidio-nl",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "presidio-analyzer",
        "presidio-anonymizer",
        "spacy",
        "transformers",
        "torch"
    ],
    entry_points={
        "console_scripts": [
            "presidio-nl=src.cli.main:run"
        ]
    },
    author="Mark Westerweel",
    author_email="markwesterweel@gmail.com",
    description="Dutch text analysis and anonymization tool using Microsoft Presidio",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Mwest2020/presidio-nl",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.8",
) 