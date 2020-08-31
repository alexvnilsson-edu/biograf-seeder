from setuptools import setup, find_packages

deps = ["click", "mysql-connector-python"]

setup(
    name="biograf",
    version="0.1",
    py_modules=[
        "biograf",
    ],
    packages=find_packages(include=["biograf_seeder", "biograf_seeder.*"]),
    install_requires=deps,
    entry_points="""
        [console_scripts]
        biograf=biograf:cli
    """,
)
