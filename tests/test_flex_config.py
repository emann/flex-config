import json

import pytest

from flex_config import FlexConfig


class TestFlexConfig:
    def test_load_sources(self):
        fc = FlexConfig()
        data = [{"a": 1, "b": {"c": 2}}, {"a": 3, "b": {"d": 4}}]
        fc.load_sources(data)
        fc.load_sources({"e": 5})

        assert fc == {"a": 3, "b": {"c": 2, "d": 4}, "e": 5}

    def test_validate(self):
        fc = FlexConfig(required={"a/b"})
        with pytest.raises(KeyError):
            fc.validate()
        fc["a/b"] = 1
        fc.validate()
        fc.required = None
        fc.validate()

    def test_flatten_dict(self):
        d = {
            "a": {"c": 1, "d": {"e": 3,},},
            "b": 2,
        }
        assert FlexConfig.flatten_dict(d) == {"a/c": 1, "a/d/e": 3, "b": 2}

    def test__value_from_string(self):
        assert 1 == FlexConfig._value_from_string("1")
        assert {"a": "b"} == FlexConfig._value_from_string('{"a": "b"}')
        assert 1.0 == FlexConfig._value_from_string("1.0")
        assert "1.0.0" == FlexConfig._value_from_string("1.0.0")

    def test_get(self):
        fc = FlexConfig()
        fc["a"] = {"b": {"c": 1}}
        assert 1 == fc["a/b/c"]
        assert 1 == fc.get("a/b/c")
        assert 3 == fc.get("b/c/d", 3)

        with pytest.raises(KeyError):
            fc["a/b/d"]

    def test_set(self):
        # Set a int by path
        path = "a/b/c"
        value = "123"
        fc = FlexConfig()
        fc[path] = value
        assert fc["a"]["b"]["c"] == int(value)

        # Set a JSON blob
        fc = FlexConfig()
        value = '{"name": "Bob"}'
        fc[path] = value
        assert fc["a"]["b"]["c"] == {"name": "Bob"}

        # This tests whether we can successfully merge two dictionaries
        config = {"integrations": {"saml": {"triax": {"idp": {"entityId": "test"}}}}}
        import_config = json.dumps({"idp": {"x509cert": "testcert"}})
        path = "integrations/saml/triax"
        fc = FlexConfig()
        fc.update(config)
        fc[path] = import_config

        assert config["integrations"]["saml"]["triax"]["idp"]["entityId"] == "test"
        assert config["integrations"]["saml"]["triax"]["idp"]["x509cert"] == "testcert"
