from pathlib import Path

import pytest

from flex_config.file_sources import FileSource


class DummyFileSource(FileSource):
    def _load_file(self, _file):
        pass


def test___init__():
    file_source = DummyFileSource(Path("supercoolpath"))

    assert file_source.path == Path("supercoolpath")

    with pytest.raises(FileNotFoundError):
        DummyFileSource(Path("supercoolpath"), path_must_exist=True)


def test_items(mocker):
    file_source = DummyFileSource(Path("supercoolpath"))
    mock_path = mocker.Mock()
    mocker.patch.object(file_source, "path", mock_path)

    mock_path.exists.return_value = False
    assert file_source.items() == []

    mock_path.exists.return_value = True

    class MockedFile:
        def __enter__(self):
            return 7

        def __exit__(self, *args):
            pass

    mock_path.open.return_value = MockedFile()

    load_sources = mocker.patch.object(file_source, "_load_file", return_value=[])
    with pytest.raises(ValueError):
        file_source.items()
    load_sources.assert_called_once_with(7)
    load_sources.reset_mock()

    data = {1: "one", "two": 2}
    load_sources.return_value = data
    assert file_source.items() == data.items()
    load_sources.assert_called_once_with(7)
