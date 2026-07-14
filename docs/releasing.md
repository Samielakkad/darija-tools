# Releasing

Releases use PyPI trusted publishing; no long-lived PyPI token is stored in GitHub.
The workflow builds distributions in an unprivileged job, then passes those exact
artifacts to the OIDC-enabled publishing job.

1. Confirm CI passes on `main` and the version matches in `pyproject.toml`, `src/darija_tools/__init__.py`, `CHANGELOG.md`, and `CITATION.cff`.
2. Build locally with `python -m build` and validate with `python -m twine check dist/*`.
3. Configure the PyPI trusted publisher for repository `Samielakkad/darija-tools`, workflow `publish.yml`, environment `pypi`.
4. Create and publish the matching GitHub release from the version tag.
5. Confirm the build and protected `pypi` environment jobs complete.
6. Verify `pip install darija-tools` and `darija --version` in a clean environment.

Publishing a GitHub release triggers `.github/workflows/publish.yml`. The publish
action generates package attestations by default when trusted publishing is used.
