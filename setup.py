import os
from pathlib import Path

import setuptools

version = os.environ.get("GITHUB_REF_NAME")
if version and version.startswith("v"):
    version = version[1:]
else:
    version = "0.0.1.dev0"

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="pdbacktester",
    version=version,
    description="Simple backtesting engine for pandas.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=["pandas", "pandera"],
)
