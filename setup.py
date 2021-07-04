import setuptools

setuptools.setup(
    name="pdbacktester",
    version="0.0.1",
    description="Simple backtesting engine for pandas.",
    packages=setuptools.find_packages(),
    install_requires=["pandas", "pandera"],
)
