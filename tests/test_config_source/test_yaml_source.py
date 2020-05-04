from pathlib import Path

import yaml

from flex_config import YAMLSource


class TestYAMLSource:
    def test___init__(self):
        yamls = YAMLSource("apathy")

        assert yamls.path == "apathy"

    def test_items(self):

        path = Path("test.yml")
        if path.exists():
            path.unlink()

        yamls = YAMLSource(path)

        assert yamls.items() == [], "items() failed when YAML file didn't exist"

        with path.open("w") as test_yaml_file:
            test_yaml_file.write(yaml.dump({"blah": 16, "blah/blah": 36,}))

        results = {}
        for key, value in yamls.items():
            results[key] = value

        assert results == {
            "blah": 16,
            "blah/blah": 36,
        }
        path.unlink()
