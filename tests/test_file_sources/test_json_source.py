from pathlib import Path

from flex_config import JSONSource


def test__load_file(mocker):
    data = {1: "one", "two": 2}
    load_json = mocker.patch("json.load", return_value=data)

    mocked_file = mocker.Mock()
    ys = JSONSource(Path("supercoolpath"))
    assert ys._load_file(mocked_file) == data
    load_json.assert_called_once_with(mocked_file)
