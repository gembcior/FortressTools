import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="FortressTools",
    version="0.0.4",
    author="mywayof.dev",
    author_email="gembcior@gmail.com",
    description="Personal Tools for development",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gembcior/FortressTools.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OTHER",
        "Operating System :: POSIX",
        "Private :: Do Not Upload to public pypi server"
    ],
    python_requires='>=3.6',
)
