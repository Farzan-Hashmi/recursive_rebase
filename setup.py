from setuptools import setup, find_packages

setup(
    name="recursive_rebase",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "recursive-rebase = recursive_rebase.main:main",
        ],
    },
)
