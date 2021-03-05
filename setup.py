import os
from setuptools import find_packages, setup
from discordproxy import __version__

# read the contents of your README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="discordproxy",
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    license="MIT",
    description="Discord Proxy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/ErikKalkoken",
    author="Erik Kalkoken",
    author_email="kalkoken87@gmail.com",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires="~=3.6",
    install_requires=["discord.py", "grpcio-tools", "grpclib"],
    entry_points={
        "console_scripts": [
            "discordproxyserver=discordproxy.server:main",
        ],
    },
)
