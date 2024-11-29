![Docker Pulls](https://img.shields.io/docker/pulls/veerendra2/kompozit) ![PyPI - Status](https://img.shields.io/pypi/status/kompozit) ![PyPI - Version](https://img.shields.io/pypi/v/kompozit)

[![Release](https://github.com/veerendra2/kompozit/actions/workflows/release.yml/badge.svg)](https://github.com/veerendra2/kompozit/actions/workflows/release.yml)

# Kompozit

> 🚧 This tool is currently under development!

Declarative Configuration Management Tool for Docker Compose.

_Like [`kustomize.io`](https://kustomize.io/), but for [Docker Compose](https://docs.docker.com/compose/)._

## Features

Kompozit simplifies complex Docker Compose setups using declarative overlays, supporting:

- **[`patchesJSON6902`](https://datatracker.ietf.org/doc/html/rfc6902)**: Precise modifications with JSON Merge Patch.
- **[`patchesStrategicMerge`](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-api-machinery/strategic-merge-patch.md)**: Flexible hierarchical changes with Strategic Merge Patch.

## Resources

- 📖 [Documentation](https://veerendra2.gitbook.io/kompozit)
- 🛠️ [Examples](https://github.com/veerendra2/kompozit/tree/main/examples)

## But Why...? 🤔

There are scenarios where you might need different Docker Compose configurations for the same application on different machines.

- For example, I use slightly different configurations for the Traefik reverse proxy when managing my public WordPress site versus my home server. Instead of maintaining multiple, slightly different `docker-compose.yml` files for the same app, you can use kompozit to simplify and manage these variations efficiently.

Additionally, kompozit allows you to combine multiple `docker-compose.yml` files into a single stack.

- For instance, you can keep a generic `docker-compose.yml` for PostgreSQL in a central location and customize it for different stacks in other locations as needed.

## Installation 💻

### PyPi

> https://pypi.org/project/kompozit/

```bash
python -m pip install kompozit

kompozit --help
usage: kompozit [-h] [-b BUILD_PATH] [-o OUTPUT_DIR] [-v]

Declarative Configuration Management Tool for Docker Compose.

options:
  -h, --help            show this help message and exit
  -b, --build BUILD_PATH
                        Path to a directory containing 'komposition.yaml'. (default: .)
  -o, --output-dir OUTPUT_DIR
                        Directory to save the generated Docker Compose files. (default: None)
  -v, --version         Show kompozit version
```

### Docker

> https://hub.docker.com/r/veerendra2/kompozit

```bash
docker pull veerendra2/kompozit
```

## Usage ⚙️

```bash
git clone git@github.com:veerendra2/kompozit.git
cd kompozit
python -m pip install .

kompozit --build ./examples/overlay
...

# inside docker
docker pull kompozit:latest
docker run -it --rm -v ./examples:/examples kompozit:latest -b /examples/overlay
```

## Local Development 🔧

```bash
git clone git@github.com:veerendra2/kompozit.git
cd kompozit

python -m venv venv
source venv/bin/activate
pip install -e .
```
