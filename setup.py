import setuptools

setuptools.setup(
    name="meroxa-py",
    version="0.0.1",
    author="Meroxa",
    author_email="dev@meroxa.io",
    url="https://github.com/meroxa/meroxa-py",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
