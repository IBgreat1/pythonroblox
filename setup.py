import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pythonroblox",
    version="0.0.1",
    author="IBgreat1",
    author_email="shamimumthaz72@gmail.com",
    description="A Package related to Roblox API , providing Way to Users as well as Groups API. More Features Coming Soon.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IBgreat1/pyroblox",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8.5'
)
