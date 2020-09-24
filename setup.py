import setuptools
import os

def get_scripts_list():
    scripts_list = os.listdir("app")
    scripts_list = ["app/" + x for x in scripts_list]
    return scripts_list

with open("README.md", "r") as f:
    long_description = f.read()


setuptools.setup(
    name="FortressTools",
    author="mywayof.dev",
    author_email="gembcior@gmail.com",
    description="Personal Tools for development",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gembcior/FortressTools.git",
    include_package_data=True,
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    packages=setuptools.find_packages(),
    scripts=get_scripts_list(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OTHER",
        "Operating System :: POSIX",
        "Private :: Do Not Upload to public pypi server"
    ],
    python_requires='>=3.6',
    install_requires=[
        'pyyaml',
        'coloredlogs',
        'diff_match_patch'
    ],
)
