# -*- coding: utf-8 -*-
"""
Kompozit
"""
import argparse
import os
import sys

import jsonpatch
import yaml
from deepmerge import Merger
from jsonpatch import JsonPatchConflict
from jsonpointer import JsonPointerException

__version__ = "0.1.0-beta"


CONFIG_FILE_NAMES = ["kompozition.yaml", "kompozition.yml"]
CUSTOM_MERGER = Merger(
    [(list, "override"), (dict, "merge")],
    ["override"],
    ["override"],
)


def parse_arguments():
    """Argument parser"""
    parser = argparse.ArgumentParser(
        description="Declarative Configuration Management Tool for Docker Compose.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-b",
        "--build",
        default=".",
        dest="build_path",
        type=str,
        required=False,
        help="Path to a directory containing 'komposition.yaml'.",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=str,
        required=False,
        help="Directory to save the generated Docker Compose files.",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s v{__version__}",
        help="Show kompozit version",
    )
    return parser.parse_args()


def find_config_file(overlay_path):
    """Find kompozition file"""
    for file_name in CONFIG_FILE_NAMES:
        file_path = os.path.join(overlay_path, file_name)
        if os.path.isfile(file_path):
            return file_name
    raise FileNotFoundError(
        "Unable to find one of 'kompozition.yaml' or 'kompozition.yml'"
        + f" in directory {os.path.abspath(overlay_path)}"
    )


def load_yaml(file_path):
    """Load YAML file"""
    with open(file_path, encoding="utf-8") as file:
        return yaml.safe_load(file)


def resolve_paths(overlay_path):
    """Resolve absloute paths of resources and patch files"""
    config_file_name = find_config_file(overlay_path)
    overlay = load_yaml(os.path.join(overlay_path, config_file_name))

    resolved_resources = []
    resolved_patches_strategic_merges = []
    merged_patches = overlay.get("patchesJSON6902", []).copy()

    for resource in overlay.get("resources", []):
        resource_path = os.path.abspath(os.path.join(overlay_path, resource))
        if os.path.isdir(resource_path):
            base = resolve_paths(resource_path)
            resolved_resources.extend(base["resources"])
            resolved_patches_strategic_merges.extend(
                base.get("patchesStrategicMerge", [])
            )
            merged_patches.extend(base.get("patchesJSON6902", []))

        elif os.path.isfile(resource_path):
            resolved_resources.append(resource_path)

    for patch in overlay.get("patchesStrategicMerge", []):
        patch_path = os.path.abspath(os.path.join(overlay_path, patch["path"]))
        resolved_patches_strategic_merges.append({"path": patch_path})

    # Replace resources with resolved ones
    overlay["resources"] = resolved_resources
    overlay["patchesStrategicMerge"] = resolved_patches_strategic_merges
    overlay["patchesJSON6902"] = merged_patches
    return overlay


def apply_patches(config, output_dir):
    """Apply patches to resources"""
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    resources = config.get("resources", [])
    json_patches = config.get("patchesJSON6902", [])
    patches_strategic_merge = config.get("patchesStrategicMerge", [])

    for resource in resources:
        resource_data = load_yaml(resource)

        # patchesJSON6902
        for patch in json_patches:
            try:
                patch_obj = jsonpatch.JsonPatch(patch["patch"])
                resource_data = patch_obj.apply(resource_data)
            except (JsonPointerException, JsonPatchConflict):
                continue

        # patchesStrategicMerge
        for patch in patches_strategic_merge:
            patch_base_file = os.path.splitext(os.path.basename(patch["path"]))[0]
            resource_base_file = os.path.splitext(os.path.basename(resource))[0]
            if resource_base_file == patch_base_file.replace("-patch", ""):
                patch_data = load_yaml(patch["path"])
                resource_data = CUSTOM_MERGER.merge(resource_data, patch_data)

        if output_dir:
            output_file = os.path.join(output_dir, os.path.basename(resource))
            with open(output_file, encoding="utf-8" "w") as file:
                yaml.dump(resource_data, file, indent=2)
        else:
            print("---")
            yaml.dump(resource_data, stream=sys.stdout, indent=2, default_flow_style=False)


def main():
    """Main function"""
    args = parse_arguments()
    resolved_komposition = resolve_paths(args.build_path)
    apply_patches(resolved_komposition, args.output_dir)
