from setuptools import setup,find_packages
from typing import List
HYPHEN_E_D = '-e .'
def get_requirements(file_path) -> List[str]:
    with open(file_path) as f:
        requirements = f.readlines()
        requirements = [req.strip() for req in requirements if req.strip()]
        if HYPHEN_E_D in requirements:
            requirements.remove(HYPHEN_E_D)
    return requirements






setup(
    name  = "my_package",
    version = "0.1.0",
    author = "Shivam Bhardwaj",
    email  = "shubhambhardwaj20232024@gmail.com",
    packages = find_packages(),
    install_requires = get_requirements('requirements.txt')
)