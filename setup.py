import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="algo_util-cpcepa",
    version="0.0.1",
    author="cpcepa",
    author_email="poulocp@hotmail.com",
    description="algo_util for modstore ai",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cpcepa/algo_util",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)