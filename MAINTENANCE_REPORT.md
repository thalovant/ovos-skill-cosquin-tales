Last Edit: Claude Opus 5.5 - 2026-11-07 - Motive: Release this fork as a wheel on Thalovant's skill index instead of a Git install.

# Maintenance report (Thalovant fork)

## 2026-11-07 - Thalovant builds carry a local version label

**Why.** Thalovant's Story Time runtime installed this fork from Git
(`git+https://github.com/thalovant/ovos-skill-cosquin-tales.git@d756874`), and that install is
the reason its pod mounted a GitHub credential. The runtime can install a pinned
wheel from Thalovant's private skill index instead, but this fork's version
(`0.1.4`) is also on PyPI as upstream's release, with different code. uv
reads the index beside PyPI, so a wheel with the same number could lose to
upstream's.

**Change.**

- `version.py` gains `VERSION_LOCAL = "thalovant.1"`, and `setup.py`'s
  `get_version()` appends it: the build is `0.1.4+thalovant.1`. PyPI never
  accepts a local version, so `==0.1.4+thalovant.1` can only match Thalovant's
  wheel.
- `publish.yml` (upstream's PyPI release) ignores `v*+thalovant.*` tags.
- `tests/test_version.py` checks the built version: upstream's public number
  from `version.py`, then `thalovant.N`, in canonical PEP 440 form.

**Releasing.** Tag the commit `v0.1.4+thalovant.1`, build the wheel from the tag
(`python -m build --wheel`), and have a Thalovant admin upload it to the
fork's catalog row with `POST /v1/marketplace/skills/{id}/versions`
(multipart). This public fork cannot call the private reusable release
workflow in `thalovant/skill-index`, so there is no release workflow here.
Any later Thalovant release of new code bumps `N`; the index refuses a second
wheel under the same version.

**Verification.** `pytest tests` on Python 3.12: 119 passed (with `requirements-test.txt`). `python setup.py --version` prints `0.1.4+thalovant.1`. The wheel built from this branch, `ovos_skill_cosquin_tales-0.1.4+thalovant.1-py3-none-any.whl`, holds the same files as a wheel built from the live commit `d756874` except `version.py`, and passes the Thalovant API's `validate_wheel`. uv resolves `==0.1.4+thalovant.1` to it with PyPI beside the index.

**Transparency Report.** AI Model: Claude Opus 5.5 (`claude-opus-5-5`) in
Claude Code. Actions Taken: wrote the version label, the tag filter, the test
and this report; ran the test suite. Oversight: prepared for the owner's
review as a pull request; not merged or released by the AI.
