import setuptools

with open("../README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

__version__ = "0.1.0"

REPO_NAME = "smart-seo-assistant-ace"
AUTHOR_USER_NAME = "SaudIqbalS"  # Replace with your GitHub username
SRC_REPO = "smart-seo-assistant-backend"
AUTHOR_EMAIL = "saudsandhila786@gmail.com"  # Replace with your email

setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="Smart SEO Assistant Backend - AI-powered SEO content generation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },
    packages=setuptools.find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "fastapi",
        "uvicorn[standard]",
        "pydantic",
        "requests",
        "beautifulsoup4",
        "requests-html",
        "lxml",
        "aiohttp",
        "tldextract",
        "pytrends",
        "nltk",
        "spacy",
        "python-dotenv",
        "PyYAML",
        "faiss-cpu",
        "sentence-transformers",
        "langchain",
        "qdrant-client",
        "openai",
        "tiktoken",
        "mlflow",
        "pandas",
        "python-box==6.0.2",
        "ensure==1.0.4",
        "tqdm",
        "joblib",
        "dvc",
        "dvc[gdrive]",
        "matplotlib",
        "seaborn",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
            "black",
            "flake8",
            "isort",
            "mypy",
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
