from setuptools import setup, find_packages

setup(
    name="xyz-pipeline",
    version="0.0.1",
    description="Generic Pipeline Mechanism",
    python_requires=">=3.4",
    author="Mozilla IT Enterprise Systems",
    author_email="jspiropulo@mozilla.com",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=["behave", "mock"],
    project_urls={"Source": "https://github.com/mozilla-it/xyz-pipeline",},
    test_suite="pipeline.tests.bdd",
    data_files=[],
)