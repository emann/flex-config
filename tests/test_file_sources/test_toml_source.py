from pathlib import Path

from flex_config import TOMLSource


def test__load_file(mocker):
    data = {1: "one", "two": 2}
    load_toml = mocker.patch("toml.load", return_value=data)

    mocked_file = mocker.Mock()
    toml_source = TOMLSource(Path("supercoolpath"))
    assert toml_source._load_file(mocked_file) == data
    load_toml.assert_called_once_with(mocked_file)
