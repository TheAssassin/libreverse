from setuptools import find_packages, setup

tests_require=[
    "tox",
    "pytest",
    "lxml",
    "cssselect",
]


setup(
    name="libreverse",
    packages=find_packages(),
    install_requires=[
        "Flask>=1.1",
        "Frozen-Flask",
    ],
    tests_require=tests_require,
    extras_require={
        "test": tests_require,
    },
)
