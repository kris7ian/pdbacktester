import os

import setuptools

version = os.environ.get("GITHUB_REF_NAME")

if version and version.startswith("v"):
    version = version[1:]
else:
    version = "0.0.1.dev0"

setuptools.setup(
    name="pdbacktester",
    version=version,
    description="Simple backtesting engine for pandas.",
    packages=setuptools.find_packages(),
    install_requires=["pandas", "pandera"],
)
