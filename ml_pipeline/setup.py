import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


__version__ = "0.1.0"

REPO_NAME = "smart-seo-assistant-ace-1"
AUTHOR_USER_NAME = "SaudIqbalS"  # Replace with your GitHub username
SRC_REPO = "smart-seo-assistant-ace"
AUTHOR_EMAIL = "saudsandhila786@gmail.com"  # Replace with your email


setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="Smart SEO Assistant ML Pipeline - AI-powered SEO content generation with ACE",
    long_description=long_description,
    long_description_content="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src")
)