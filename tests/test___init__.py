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
    s1 = {"key": "val"}
    s2 = {"other": "stuff"}
    s3 = {"super": "unique"}
    s4 = mocker.Mock(return_value={"dynamic": "source1"})

    def _mock_merge_sources(dest, source):
        dest = dest.copy()
        dest.update(source)
        return dest

    mocker.patch("flex_config._merge_sources", _mock_merge_sources)

    assert _compile_sources(s1) == s1

    assert _compile_sources([s1, s2, s3, s4]) == {
        "key": "val",
        "other": "stuff",
        "super": "unique",
        "dynamic": "source1",
    }
    expected_s4_param = {
        "key": "val",
        "other": "stuff",
        "super": "unique",
    }
    s4.assert_called_with(expected_s4_param)


def test_construct_config(mocker):
    sources = [{}, {}, {}]
    mocker.patch("flex_config.issubclass", return_value=False)
    with pytest.raises(TypeError):
        construct_config(config_schema={}, sources=sources)

    compile_sources = mocker.patch("flex_config._compile_sources", return_value={"compiled": "sources"})
    mocker.patch("flex_config.issubclass", return_value=True)
    config_schema = mocker.Mock()

    construct_config(config_schema=config_schema, sources=sources)
    compile_sources.assert_called_with(sources=sources)
    config_schema.assert_called_with(**{"compiled": "sources"})
