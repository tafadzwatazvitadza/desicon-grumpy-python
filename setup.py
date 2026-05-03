from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="desicon-grumpy",
    version="1.0.3",
    author="Desicon Platform",
    author_email="hello@desicon.ai",
    description="Zero-config AI SRE companion that aggressively roasts your crashes.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tafadzwatazvitadza/desicon-grumpy-python",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        "requests>=2.25.1",
    ],
)
