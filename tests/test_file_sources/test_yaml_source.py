from pathlib import Path

from flex_config import YAMLSource


def test__load_file(mocker):
    data = {1: "one", "two": 2}
    load_yaml = mocker.patch("yaml.safe_load", return_value=data)

    mocked_file = mocker.Mock()
    ys = YAMLSource(Path("supercoolpath"))
    assert ys._load_file(mocked_file) == data
    load_yaml.assert_called_once_with(mocked_file)
