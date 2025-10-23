import glob
import os
import yaml


def test_github_workflows_are_valid_yaml():
    """Load every YAML file under .github/workflows to ensure they're valid YAML.

    This test will fail fast during CI if any workflow contains invalid YAML
    syntax.
    """
    base = os.path.join(os.path.dirname(__file__), "..")
    workflows_dir = os.path.join(base, ".github", "workflows")
    assert os.path.isdir(workflows_dir), ".github/workflows directory not found"

    patterns = ["*.yml", "*.yaml"]
    files = []
    for p in patterns:
        files.extend(glob.glob(os.path.join(workflows_dir, p)))

    assert files, "No workflow files found in .github/workflows"

    for f in sorted(files):
        with open(f, "r", encoding="utf-8") as fh:
            try:
                yaml.safe_load(fh)
            except Exception as e:
                raise AssertionError(f"YAML parse error in {f}: {e}") from e
