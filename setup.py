import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="FortressTools",
    version="0.0.2",
    author="mywayof.dev",
    author_email="mywayof.dev@gmail.com",
    description="Personal Tools for development",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://gogs.gembcior.pl/Gembcior/FortressTools.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OTHER",
        "Operating System :: POSIX",
        "Private :: Do Not Upload to public pypi server"
    ],
    python_requires='>=3.6',
)
