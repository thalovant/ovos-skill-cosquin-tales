"""The version this fork builds: upstream's number plus Thalovant's local label."""
import re
import subprocess
import sys
from pathlib import Path

from packaging.version import Version

ROOT = Path(__file__).resolve().parents[1]


def _version_block():
    values = {}
    for line in (ROOT / "version.py").read_text().splitlines():
        if "# END_VERSION_BLOCK" in line:
            break
        name, sep, value = line.partition("=")
        if sep and name.strip().startswith("VERSION_"):
            values[name.strip()] = value.strip().strip("\"'")
    return values


def _built_version():
    result = subprocess.run(
        [sys.executable, "setup.py", "--version"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip().splitlines()[-1]


def test_the_build_carries_upstreams_number_and_a_thalovant_local_label():
    block = _version_block()
    version = Version(_built_version())

    assert version.public == (
        f"{block['VERSION_MAJOR']}.{block['VERSION_MINOR']}.{block['VERSION_BUILD']}"
    )
    assert re.fullmatch(r"thalovant\.[0-9]+", version.local)
    assert version.local == block["VERSION_LOCAL"]


def test_the_version_string_is_canonical_so_the_tag_and_wheel_name_agree():
    built = _built_version()
    assert str(Version(built)) == built
