from setuptools import setup  # type: ignore

with open("README.md", "r") as f:
    long_description = f.read()


setup(
    name="typed-monads",
    version="0.4.8",
    author="Correl Roush, Sam Reghenzi",
    author_email="correl@gmail.com, sammyrulez@gmail.com",
    description="Type-annotated monad implementations for Python 3.7+",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sammyrulez/typed-monads",
    packages=["monads"],
    package_data={"monads": ["py.typed"]},
    include_package_data=True,
    setup_requires=["pytest-runner"],
    tests_require=[
        "pytest",
        "black",
        "mypy",
        "pytest-asyncio",
        "pytest-cov",
        "pytest-black",
        "pytest-mypy",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries",
    ],
)
