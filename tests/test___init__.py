import pytest

from flex_config import _compile_sources, _merge_sources, construct_config


def test__merge_sources():
    d1 = {"fruits": ["apple", "banana", "mango"], "nested": {"dont": "touch", "change": "me"}, "number": 7}
    d1_copy = d1.copy()

    d2 = {"fruits": ["mango", "guava"], "nested": {"change": "this one", "anew": "key"}, "state": "CT"}
    d2_copy = d2.copy()

    c = {}
    _merge_sources(c, d1)
    assert c == d1
    assert not c is d1

    _merge_sources(c, d2)
    assert c == {
        "fruits": ["mango", "guava"],
        "nested": {"dont": "touch", "change": "this one", "anew": "key"},
        "number": 7,
        "state": "CT",
    }
    # Check we didn't accidentally alter the original sources
    assert d1 == d1_copy
    assert d2 == d2_copy


def test__compile_sources(mocker):
    d1 = {"key": "val"}
    d2 = {"other": "stuff"}
    d3 = {"super": "unique"}

    merge_sources = mocker.patch("flex_config._merge_sources", return_value={"banana": "phone"})

    assert _compile_sources(d1) == {"banana": "phone"}
    merge_sources.assert_called_once_with(dest=mocker.ANY, source=d1)
    merge_sources.reset_mock()

    assert _compile_sources([d1, d2, d3]) == {"banana": "phone"}
    for source_dict in [d1, d2, d3]:
        merge_sources.assert_any_call(dest=mocker.ANY, source=source_dict)
    assert merge_sources.call_count == 3

    source = mocker.Mock()
    mocker.patch("flex_config.isinstance", return_value=True)
    assert _compile_sources([source]) == {"banana": "phone"}
    source.dict.assert_called_once()


def test_construct_config(mocker):
    sources = [{}, {}, {}]
    with pytest.raises(TypeError):
        construct_config(config_schema={}, sources=sources)

    compile_sources = mocker.patch("flex_config._compile_sources", return_value={"compiled": "sources"})
    mocker.patch("flex_config.isinstance", return_value=True)
    config_schema = mocker.Mock()

    construct_config(config_schema=config_schema, sources=sources)
    compile_sources.assert_called_with(sources=sources)
    config_schema.assert_called_with(**{"compiled": "sources"})
