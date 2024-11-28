import os
import tempfile
import unittest
import yaml
from unittest.mock import patch, MagicMock
from kompozit import resolve_paths, apply_patches, load_yaml

class TestKompozit(unittest.TestCase):
    def setUp(self):
        # Create temporary directories and files for testing
        self.test_dir = tempfile.TemporaryDirectory()
        self.overlay_path = self.test_dir.name
        self.resource_file = os.path.join(self.overlay_path, "resource.yaml")
        self.patch_file = os.path.join(self.overlay_path, "patch.yaml")
        self.config_file = os.path.join(self.overlay_path, "kompozition.yaml")

        # Write test YAML files
        with open(self.config_file, "w", encoding="utf-8") as file:
            yaml.dump({
                "resources": ["resource.yaml"],
                "patchesStrategicMerge": [{"path": "patch.yaml"}],
                "patchesJSON6902": [{"patch": [{"op": "replace", "path": "/key1", "value": "new_value"}]}]
            }, file)

        with open(self.resource_file, "w", encoding="utf-8") as file:
            yaml.dump({"key1": "value1", "key2": "value2"}, file)

        with open(self.patch_file, "w", encoding="utf-8") as file:
            yaml.dump({"key2": "merged_value"}, file)

    def tearDown(self):
        # Cleanup temporary directories
        self.test_dir.cleanup()

    def test_resolve_paths_positive(self):
        # Test resolving paths with valid config
        resolved_config = resolve_paths(self.overlay_path)
        self.assertIn("resources", resolved_config)
        self.assertIn("patchesStrategicMerge", resolved_config)
        self.assertIn("patchesJSON6902", resolved_config)
        self.assertEqual(len(resolved_config["resources"]), 1)
        self.assertTrue(os.path.isabs(resolved_config["resources"][0]))

    def test_resolve_paths_negative(self):
        # Test with missing config file
        with self.assertRaises(FileNotFoundError):
            resolve_paths("non_existent_path")

    def test_apply_patches_positive(self):
        # Test applying patches with output directory
        output_dir = os.path.join(self.overlay_path, "output")
        resolved_config = resolve_paths(self.overlay_path)
        apply_patches(resolved_config, output_dir)

        output_file = os.path.join(output_dir, "resource.yaml")
        self.assertTrue(os.path.exists(output_file))

        with open(output_file, "r", encoding="utf-8") as file:
            output_data = yaml.safe_load(file)

        self.assertEqual(output_data["key1"], "new_value")  # JSON patch applied
        self.assertEqual(output_data["key2"], "merged_value")  # Strategic merge patch applied

    def test_apply_patches_negative(self):
        # Test applying patches with invalid resource file
        invalid_resource_file = os.path.join(self.overlay_path, "invalid.yaml")
        with open(self.config_file, "w", encoding="utf-8") as file:
            yaml.dump({"resources": ["invalid.yaml"]}, file)

        resolved_config = resolve_paths(self.overlay_path)
        with self.assertRaises(FileNotFoundError):
            apply_patches(resolved_config, None)

    @patch("sys.stdout", new_callable=MagicMock)
    def test_apply_patches_print(self, mock_stdout):
        # Test applying patches and printing to stdout
        resolved_config = resolve_paths(self.overlay_path)
        apply_patches(resolved_config, None)

        # Check if "---" and YAML data are printed
        self.assertIn("---", mock_stdout.write.call_args_list[0][0][0])

if __name__ == "__main__":
    unittest.main()