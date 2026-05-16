# MyPublicIp

MyPublicIp is a Python module that retrieves the public IP address of the current connection using a simple command-line interface.

## Features

- Retrieves the public IP address using the `curl` command.
- Logs the retrieval process and any errors encountered.

## Installation

You can install MyPublicIp using pip. First, ensure you have Python 3 and pip installed on your system. Then run:

```
pip install mypublicip
```

## Usage

To use the module, you can run the script directly from the command line:

```
python -m mypublicip.mypublicip
```

This will output your current public IP address.

## Requirements

- Python 3.x
- `curl` must be installed on your system.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## 🔄 Pipeline CI/CD

Le pipeline GitLab CI/CD est standardisé et s'exécute automatiquement sur `main`, `master` et les tags.

| Stage | Job | Description |
|-------|-----|-------------|
| `test` | `test:quality` | Vérifie la structure du projet |
| `build` | `build:package` | Construit le package Python (wheel + sdist) |
| `publish` | `publish:nexus` | Publie sur Nexus PyPI (si version absente) |
| `publish` | `cleanup:on_failure` | Nettoyage en cas d'échec |
| `mirror` | `mirror:github` | Miroir vers GitHub via HTTPS |

- **Runtime** : Python 3.11 (`python:3.11-slim`)
- **Publication** : contrôlée — upload ignoré si la version est déjà présente sur Nexus
- **Credentials** : gérés par `jeyriku-vault` (chiffrement AES-256)
- **Mirror GitHub** : automatique sur push vers GitLab
