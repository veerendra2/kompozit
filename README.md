# Kompozit

> :construction_worker: This tool is currently in beta and still under development!

Declarative Configuration Management Tool for Docker Compose.

_Like [`kustomize`](https://kustomize.io/), but for [Docker Compose](https://docs.docker.com/compose/)._

Kompozit provides flexible, declarative overlays to manage complex Docker Compose configurations with support for:

- **[`patchesJSON6902`](https://datatracker.ietf.org/doc/html/rfc6902)**: JSON Merge Patch for precise modifications.
- **[`patchesStrategicMerge`](https://stackoverflow.com/q/71165168/2200798)**: Strategic Merge Patch for hierarchical changes.

## But Why...? :thinking:

There are scenarios where you might need different Docker Compose configurations for the same application on different machines.

- For example, I use slightly different configurations for the Traefik reverse proxy when managing my public WordPress site versus my home server. Instead of maintaining multiple, slightly different `docker-compose.yml` files for the same app, you can use kompozit to simplify and manage these variations efficiently.

Additionally, kompozit allows you to combine multiple `docker-compose.yml` files into a single stack.

- For instance, you can keep a generic `docker-compose.yml` for PostgreSQL in a central location and customize it for different stacks in other locations as needed.

## Installation :computer:

```bash
python -m pip install kompozit
```

## Usage :gear:

```bash
git clone git@github.com:veerendra2/kompozit.git
cd kompozit
python -m pip install .

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

kompozit --build ./examples/overlay

# inside docker
docker pull kompozit:latest
docker run -it --rm -v ./examples:/examples kompozit:latest -b /examples/overlay
```

## Local Development :wrench:

```bash
git clone git@github.com:veerendra2/kompozit.git
cd kompozit

python -m venv venv
source venv/bin/activate
pip install -e .
```
