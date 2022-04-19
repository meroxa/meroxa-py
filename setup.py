import setuptools

# Metadata is in setup.cfg, this is for GitHub's dependency graph
setuptools.setup(
    name="meroxa-py",
    install_requires=[
        "aiohttp >= 3.8.1"
    ],
)
