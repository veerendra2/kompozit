#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os

import jsonpatch
import yaml
from deepmerge import Merger, always_merger
from jsonpatch import JsonPatchConflict
from jsonpointer import JsonPointerException

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


# Define custom merge strategy to overwrite arrays
custom_merger = Merger(
    [(list, "override"), (dict, "merge")],  # Overwrite lists, merge dictionaries
    ["override"],  # Fallback to overriding
    ["override"],  # Default strategy
)


def get_paths(kom_path):
    """Recursively get all absolute resource paths and update patches paths."""
    config_file_name = find_config_file(kom_path)
    overlay = load_yaml(os.path.join(kom_path, config_file_name))

    # Process resources and resolve absolute paths
    resolved_resources = []
    resolved_patches_strategic_merges = []
    merged_patches = overlay.get("patchesJSON6902", []).copy()

    for resource in overlay.get("resources", []):
        resource_path = os.path.abspath(os.path.join(kom_path, resource))
        if os.path.isdir(resource_path):
            base = get_paths(resource_path)
            resolved_resources.extend(base["resources"])
            resolved_patches_strategic_merges.extend(
                base.get("patchesStrategicMerge", [])
            )
            merged_patches.extend(base.get("patchesJSON6902", []))

        elif os.path.isfile(resource_path):
            resolved_resources.append(resource_path)

    for patch in overlay.get("patchesStrategicMerge", []):
        patch_path = os.path.abspath(os.path.join(kom_path, patch["path"]))
        resolved_patches_strategic_merges.append({"path": patch_path})

    # Replace resources and patches with resolved ones
    overlay["resources"] = resolved_resources
    overlay["patchesStrategicMerge"] = resolved_patches_strategic_merges
    overlay["patchesJSON6902"] = merged_patches
    return overlay


def apply_patches(config, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    resources = config.get("resources", [])
    json_patches = config.get("patchesJSON6902", [])
    patches_strategic_merge = config.get("patchesStrategicMerge", [])

    for resource in resources:
        with open(resource, "r") as file:
            resource_data = yaml.safe_load(file)

        for patch in json_patches:
            try:
                patch_obj = jsonpatch.JsonPatch(patch["patch"])
                resource_data = patch_obj.apply(resource_data)
            except (JsonPointerException, JsonPatchConflict):
                # Ignore patches that can't be applied
                continue

        # Write the patched resource to a new file
        output_file = os.path.join(output_dir, os.path.basename(resource))
        with open(output_file, "w") as file:
            yaml.dump(resource_data, file, indent=2)

        for paths in patches_strategic_merge:

            if "paths" in patch:
                # Handle strategic merge patches from files
                patch_file = os.path.abspath(patch["paths"])
                if not os.path.isfile(patch_file):
                    continue

                with open(patch_file, "r") as patch_file_obj:
                    patch_data = yaml.safe_load(patch_file_obj)

                # Perform a strategic merge with custom merger
                resource_data = custom_merger.merge(resource_data, patch_data)


def main():
    s = get_paths("overlay")
    # print(yaml.dump(s, indent=2))
    # build(s)
    apply_patches(s, "output")


if __name__ == "__main__":
    main()
