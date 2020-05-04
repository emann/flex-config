from flex_config import EnvSource


class TestEnvSource:
    def test___init__(self):
        envs = EnvSource("PRE_", separator="t")

        assert envs.prefix == "PRE_"
        assert envs.separator == "t"

    def test_items(self, mocker):
        fake_os = mocker.patch("flex_config.config_source.env_source.os")

        responses = {
            "SOMETHING_ELSE": 42,
            "PRE_BLAH": 16,
            "PRE_BLAHtBLAH": 36,
        }

        fake_os.environ = responses

        envs = EnvSource("PRE_", separator="t")

        results = {}
        for key, value in envs.items():
            results[key] = value

        assert results == {
            "blah": 16,
            "blah/blah": 36,
        }
