import pytest

from flex_config import _compile_sources, _merge_sources, construct_config, ConfigSchema


def test__merge_sources():
    dict_1 = {"fruits": ["apple", "banana", "mango"], "nested": {"dont": "touch", "change": "me"}, "number": 7}
    dict_1_copy = dict_1.copy()

    dict_2 = {"fruits": ["mango", "guava"], "nested": {"change": "this one", "anew": "key"}, "state": "CT"}
    dict_2_copy = dict_2.copy()

    config = {}
    _merge_sources(config, dict_1)
    assert config == dict_1
    assert config is not dict_1

    _merge_sources(config, dict_2)
    assert config == {
        "fruits": ["mango", "guava"],
        "nested": {"dont": "touch", "change": "this one", "anew": "key"},
        "number": 7,
        "state": "CT",
    }
    # Check we didn't accidentally alter the original sources
    assert dict_1 == dict_1_copy
    assert dict_2 == dict_2_copy


def test__compile_sources(mocker):
    source_1 = {"key": "val"}
    source_2 = {"other": "stuff"}
    source_3 = {"super": "unique"}
    source_4 = mocker.Mock(return_value={"dynamic": "source1"})
    source_5 = mocker.Mock(return_value=[{"l1": "nice"}, {"l2": "source"}, {"l3": "bro"}])

    def _mock_merge_sources(dest, source):
        dest_copy = dest.copy()
        dest_copy.update(source)
        return dest_copy

    mocker.patch("flex_config._merge_sources", _mock_merge_sources)

    assert _compile_sources(source_1) == source_1

    assert _compile_sources([source_1, source_2, source_3, source_4, source_5]) == {
        "key": "val",
        "other": "stuff",
        "super": "unique",
        "dynamic": "source1",
        "l1": "nice",
        "l2": "source",
        "l3": "bro",
    }

    expected_source_4_param = {
        "key": "val",
        "other": "stuff",
        "super": "unique",
    }
    source_4.assert_called_with(expected_source_4_param)

    expected_source_5_param = {
        "key": "val",
        "other": "stuff",
        "super": "unique",
        "dynamic": "source1",
    }
    source_5.assert_called_with(expected_source_5_param)


class MyConfig(ConfigSchema):
    a: int
    b: str


def test_construct_config(mocker):
    sources = [{"a": 1}, {"b": "two"}, {}]
    compiled_sources = {"a": 1, "b": "two"}
    mocker.patch("flex_config.issubclass", return_value=False)
    with pytest.raises(TypeError):
        construct_config(config_schema=MyConfig, sources=sources)

    compile_sources = mocker.patch("flex_config._compile_sources", return_value=compiled_sources)
    mocker.patch("flex_config.issubclass", return_value=True)

    config = construct_config(config_schema=MyConfig, sources=sources)
    compile_sources.assert_called_with(sources=sources)

    assert config == MyConfig(**compiled_sources)
