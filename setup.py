#!/usr/bin/env python3
from setuptools import setup
from os import walk, path

BASEDIR = path.abspath(path.dirname(__file__))
URL = "https://github.com/andlo/ovos-skill-cosquin-tales"
SKILL_CLAZZ = "CosquinTales"  # needs to match __init__.py class name
PYPI_NAME = "ovos-skill-cosquin-tales"  # pip install PYPI_NAME

SKILL_AUTHOR, SKILL_NAME = URL.split(".com/")[-1].split("/")
SKILL_PKG = SKILL_NAME.lower().replace("-", "_")
PLUGIN_ENTRY_POINT = f"{SKILL_NAME.lower()}.{SKILL_AUTHOR.lower()}={SKILL_PKG}:{SKILL_CLAZZ}"
BASE_PATH = path.abspath(path.join(path.dirname(__file__), "."))


def get_version():
    """Find the version of the package.

    ``VERSION_LOCAL`` is Thalovant's PEP 440 local label (``thalovant.N``).
    This fork builds upstream's version numbers with different code, and PyPI
    refuses local versions, so a pin on ``X.Y.Z+thalovant.N`` can only resolve
    to the wheel on Thalovant's skill index, never to upstream's release.
    """
    version_file = path.join(BASE_PATH, "version.py")
    values = {}
    with open(version_file) as f:
        for line in f:
            if "# END_VERSION_BLOCK" in line:
                break
            name, sep, value = line.partition("=")
            if sep and name.strip().startswith("VERSION_"):
                values[name.strip()] = value.split("#", 1)[0].strip().strip("\"'")
    version = f"{values['VERSION_MAJOR']}.{values['VERSION_MINOR']}.{values['VERSION_BUILD']}"
    alpha = values.get("VERSION_ALPHA", "0")
    if alpha and int(alpha) > 0:
        version += f"a{alpha}"
    local = values.get("VERSION_LOCAL", "")
    if local:
        version += f"+{local}"
    return version


def get_requirements(requirements_filename: str):
    requirements_file = path.join(path.dirname(__file__), requirements_filename)
    with open(requirements_file, "r", encoding="utf-8") as r:
        requirements = r.readlines()
    requirements = [r.strip() for r in requirements if r.strip() and not r.strip().startswith("#")]
    return requirements


def find_resource_files():
    resource_base_dirs = ("locale", "regex", "ui", "sounds")
    package_data = ["*.json"]
    for res in resource_base_dirs:
        if path.isdir(path.join(BASE_PATH, res)):
            for directory, _, files in walk(path.join(BASE_PATH, res)):
                if files:
                    package_data.append(path.join(directory.replace(BASE_PATH, "").lstrip("/"), "*"))
    return package_data


with open("README.md", "r") as f:
    long_description = f.read()


setup(
    name=PYPI_NAME,
    version=get_version(),
    description="Emmanuel Cosquin's Lorraine folk tales (French regional folklore) provider skill for ovos-common-reading-pipeline-plugin",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=URL,
    project_urls={
        "Source": URL,
        "Bug Tracker": f"{URL}/issues",
    },
    author="Andreas Lorensen",
    author_email="andlo@outlook.dk",
    license="GPL-3.0-or-later",
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Home Automation",
    ],
    package_dir={SKILL_PKG: "."},
    package_data={SKILL_PKG: find_resource_files()},
    packages=[SKILL_PKG],
    include_package_data=True,
    install_requires=get_requirements("requirements.txt"),
    keywords="ovos skill voice assistant fairytales folklore french lorraine storytelling",
    entry_points={"ovos.plugin.skill": PLUGIN_ENTRY_POINT},
)
