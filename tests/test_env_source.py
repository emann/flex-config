from flex_config import EnvSource


def test___init__():
    envs = EnvSource("PRE_", separator="t")

    assert envs.prefix == "PRE_"
    assert envs.separator == "t"


def test_to_dict(mocker):
    fake_os = mocker.patch("flex_config.env_source.os")

    responses = {
        "SOMETHING_ELSE": 42,
        "PRE_BLAHtBLAHtBLAH": 38,
        "PRE_BLAHtBLAHtBLAM": 39,
        "PRE_BLAHtBLAM": 7,
    }

    fake_os.environ = responses

    envs = EnvSource("PRE_", separator="t")

    assert envs.to_dict() == {
        "blah": {
            "blah": {
                "blah": 38,
                "blam": 39,
            },
            "blam": 7,
        }
    }


def test_items(mocker):
    envs = EnvSource("PRE_", separator="t")

    to_dict_return = {1: 2, 3: 4, 5: 6}
    to_dict = mocker.patch.object(envs, "to_dict", return_value=to_dict_return)

    assert envs.items() == to_dict_return.items()
    to_dict.assert_called_once()
