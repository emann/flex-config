from pathlib import Path

import pytest

from flex_config.file_sources import FileSource


class DummyFileSource(FileSource):
    def _load_file(self, v):
        pass


def test___init__():
    fs = DummyFileSource(Path("supercoolpath"))

    assert fs.path == Path("supercoolpath")

    with pytest.raises(FileNotFoundError):
        DummyFileSource(Path("supercoolpath"), path_must_exist=True)


def test_items(mocker):
    fs = DummyFileSource(Path("supercoolpath"))
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

    load_sources = mocker.patch.object(fs, "_load_file", return_value=[])
    with pytest.raises(ValueError):
        fs.items()
    load_sources.assert_called_once_with(7)
    load_sources.reset_mock()

    data = {1: "one", "two": 2}
    load_sources.return_value = data
    assert fs.items() == data.items()
    load_sources.assert_called_once_with(7)
