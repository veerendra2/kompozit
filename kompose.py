#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml
import json
import os

CONFIG_FILE_NAMES = ["komposation.yaml", "komposation.yml"]

def find_config_file(kom_path):
    for file_name in CONFIG_FILE_NAMES:
        file_path = os.path.join(kom_path, file_name)
        if os.path.isfile(file_path):
            return file_name
    raise FileNotFoundError("No valid configuration file (.yaml or .yml) found.")

def load_yaml(file_path):
    """Load YAML file."""
    with open(file_path, "r") as file:
        return yaml.safe_load(file)

def get_paths(kom_path):
    """Recursively get all absolute resource paths and update patches paths."""
    config_file_name = find_config_file(kom_path)
    overlay = load_yaml(os.path.join(kom_path, config_file_name))

    # Process resources and resolve absolute paths
    resolved_resources = []
    merged_patches = overlay.get("patches", []).copy()  # Start with current patches

    for resource in overlay.get("resources", []):
        resource_path = os.path.abspath(os.path.join(kom_path, resource))
        if os.path.isdir(resource_path):
            # Recursively get paths if it's a directory
            base_overlay = get_paths(resource_path)
            resolved_resources.extend(base_overlay["resources"])
            merged_patches.extend(base_overlay.get("patches", []))  # Merge patches
        elif os.path.isfile(resource_path):
            # Add file resource
            resolved_resources.append(resource_path)

    # Update patches' paths if they are present
    for patch in merged_patches:
        if "paths" in patch:
            patch_path = os.path.abspath(os.path.join(kom_path, patch["paths"]))
            patch["paths"] = patch_path

    # Replace resources and patches with resolved ones
    overlay["resources"] = resolved_resources
    overlay["patches"] = merged_patches
    return overlay

def build():
    pass


def main():
    s = get_paths("overlay")
    print(yaml.dump(s, indent=2))


if __name__ == "__main__":
    main()
