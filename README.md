# MyPublicIp

MyPublicIp is a small Python package and command-line tool that retrieves the public IP address of the current connection and looks up its organization and ASN.

## Requirements

- Python 3.7 or newer for the current implementation (`subprocess.run` uses `capture_output` and `text`). Package metadata currently declares Python 3.6 or newer; CI runs on Python 3.11.
- `curl` installed and available on `PATH`.
- Network access to `ifconfig.me` and `ipapi.co` for the owner and ASN lookup.

There are no third-party Python runtime dependencies. PyVault is used only for CI publication, not for IP lookup.

## Installation

From the repository root:

```sh
python -m pip install .
```

For development, use `python -m pip install -e .`.

Published packages are available through the internal Nexus PyPI repository when connected to the internal network:

```sh
python -m pip install --index-url http://jeysrv12:8081/repository/pypi-releases/simple/ --trusted-host jeysrv12 mypublicip
```

## Usage

After installation:

```sh
mypublicip
```

Alternatively, run the CLI module:

```sh
python -m mypublicip.cli
```

Example standard output:

```text
Public IP: 203.0.113.42
Owner: Example Network (AS64500)
```

The CLI also writes informational and error logs to standard error.
If the owner lookup fails or the API has no organization or ASN, the CLI still prints the IP and then `Owner and ASN: unavailable`.

### Python API

```python
from mypublicip.cli import get_public_ip, get_ip_owner

ip = get_public_ip()
if ip:
    print(ip)
    print(get_ip_owner(ip))
```

`get_public_ip()` returns the stripped response text, or `None` when curl exits with a nonzero status. An empty response produces an empty string. The response is not validated as an IP address. If curl is missing, Python raises `FileNotFoundError`.

`get_ip_owner(ip)` returns an `(organization, ASN)` tuple from [ipapi.co](https://ipapi.co/api/), or `None` when the address is invalid or the lookup is unavailable. The organization is the network organization reported by the lookup service; it may differ from the legal registrant of the IP block.

On a handled lookup failure, the CLI prints `Could not retrieve public IP.`; it does not explicitly set a nonzero exit status.

## GitLab CI/CD

The pipeline is defined in [`.gitlab-ci.yml`](.gitlab-ci.yml). Python jobs use `python:3.11-slim`.

| Stage | Job | Behavior | Runs on |
| --- | --- | --- | --- |
| `test` | `test:quality` | Checks project structure, installs the package in editable mode, and verifies import. | Branches, merge requests, tags |
| `build` | `build:package` | Builds wheel and source distributions; retains artifacts for one week. | `main`, tags |
| `publish` | `publish:nexus` | Publishes to Nexus unless the version check finds it already present. | `main`, tags |
| `publish` | `cleanup:on_failure` | Removes build outputs after a pipeline failure; allowed to fail. | On failure, subject to GitLab's default job selection |
| `tag` | `tag:version` | Creates a tag from the version in `pyproject.toml` through the GitLab API. | `main` |
| `mirror` | `mirror:github` | Force-pushes the pipeline commit to GitHub `main` and pushes tags with force. | `main`, tags |

The quality job is a structure/install/import check; it does not currently run functional IP lookup tests.

### CI credentials

Publication installs `pyvault-web>=1.1.1` and runs `python -m pyvault.client configure-nexus` to configure Nexus credentials. The pipeline no longer uses `jeyriku-vault`.

| Variable | Purpose |
| --- | --- |
| `PYVAULT_URL` | Central PyVault endpoint; defaults to `http://pyvault.int.jeyriku.net:8000` in the pipeline. |
| `PYVAULT_TOKEN` | PyVault authentication token for accessing the `nexus` credential. |
| `GITLAB_API_TOKEN` | GitLab API token used to create release tags. |
| `GITHUB_MIRROR_TOKEN` | GitHub token used to push to `jeyriku/mypublicip`. |
| `NEXUS_PYPI_URL` | Nexus publication endpoint declared in the pipeline. |

Store tokens in GitLab CI/CD variables with masking enabled and access appropriate to the branches/tags that run these jobs.

## Release helpers

Run these scripts from the repository root:

- `bash scripts/bump_version.sh X.Y.Z` updates the version in `pyproject.toml`.
- `bash scripts/release.sh` commits any staged changes, creates the version tag if absent, then pushes the current branch and that tag to `origin`.

The pipeline reads its release version from `pyproject.toml`. The legacy `setup.py` also contains a version value; the bump helper does not update it.

## License

This project is licensed under the [MIT License](LICENSE).
