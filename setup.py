from setuptools import setup, find_packages

setup(
    name="presidio-nl",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "presidio-analyzer>=2.2.0",
        "presidio-anonymizer>=2.2.0",
        "spacy>=3.0.0",
        "transformers>=4.0.0",
        "torch>=1.0.0",
        "PyPDF2>=3.0.0",
        "reportlab>=4.0.0",
        "python-docx>=0.8.11",
        "pdf2docx>=0.5.6"
    ],
    extras_require={
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-asyncio>=0.21.0",
            "psutil>=5.9.0",
            "requests>=2.31.0",
            "httpx>=0.24.0",
            "fastapi>=0.68.0"
        ]
    }
) 