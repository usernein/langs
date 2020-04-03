import re 
import setuptools

with open("README.md", "r") as fp:
    long_description = fp.read()
    
with open('requirements.txt') as fp:
    requirements = [line.strip() for line in fp]

with open('langs/__init__.py') as fp:
    version = re.search('__version__ = "(.+?)"', fp.read())[1]


setuptools.setup(
    name="langs",
    version=version,
    author="Cezar H.",
    license="LGPLv3+",
    description="tools for managing l10n strings",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/usernein/langs",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=requirements,
)