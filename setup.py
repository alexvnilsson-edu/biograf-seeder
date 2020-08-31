from setuptools import setup, find_packages

deps = ["click >= 7.1.2", "mysql-connector-python >= 8.0.21"]

setup(
    name="biograf",
    version="0.1",
    py_modules=[
        "biograf",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=deps,
    entry_points="""
        [console_scripts]
        biograf=biograf:cli
    """,
)
