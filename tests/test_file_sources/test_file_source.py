from pathlib import Path

import pytest

from flex_config.file_sources import FileSource


def test___init__():
    fs = FileSource(Path("supercoolpath"))

    assert fs.path == Path("supercoolpath")

    with pytest.raises(RuntimeError):
        FileSource(Path("supercoolpath"), path_must_exist=True)


def test__load_file():
    fs = FileSource(Path("supercoolpath"))

    with pytest.raises(NotImplementedError):
        fs._load_file(Path(__file__).open())


def test_items(mocker):
    fs = FileSource(Path("supercoolpath"))
    mock_path = mocker.Mock()
    mocker.patch.object(fs, "path", mock_path)

    mock_path.exists.return_value = False
    assert fs.items() == []

    mock_path.exists.return_value = True

    class MockedFile:
        def __enter__(self):
            return 7

        def __exit__(self, *args):
            pass

    mock_path.open.return_value = MockedFile()

    data = {1: "one", "two": 2}
    load_sources = mocker.patch("flex_config.file_sources.file_source.FileSource._load_file", return_value=data)
    assert fs.items() == data.items()
    load_sources.assert_called_once_with(7)
