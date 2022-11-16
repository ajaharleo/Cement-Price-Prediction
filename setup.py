import setuptools
from typing import List

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

__version__ = "0.0.0"

REQUIREMENTS_FILENAME = 'requirements.txt'

def get_requirements_list()->List[str]:
    """
    This function is going to return list of requirements present in requirements.txt file
    returns a list of all library names needed to be installed to run the app.
    """
    with open(REQUIREMENTS_FILENAME, 'r') as requirements_file:
        return requirements_file.readlines().remove('-e .')

REPO_NAME = "Cement-Price-Prediction"
AUTHOR_USER_NAME = "ajaharleo"
SRC_REPO = "CementStrength"
AUTHOR_EMAIL = "ajaharaj10518@outlook.com"

setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="A prediction app to predict sales of BigMart products",
    long_description=long_description,
    #long_description_content="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires = get_requirements_list()
)