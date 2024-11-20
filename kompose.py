#!/usr/bin/env python3

import yaml
import json
import os

def load_yaml(file_path):
    """Load YAML file."""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


def main():

    overlay_kompose = load_yaml("komposation.yaml")
    for resources in overlay_kompose["resources"]:
        pass

if __name__ == '__main__':
    main()
