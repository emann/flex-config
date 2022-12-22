from flex_config import AWSSource


def test___init__(mocker):
    import boto3

    def _client(service, region, **kwargs):
        client_data = {"service": service, "region": region}
        client_data.update(kwargs)
        return client_data

    mocker.patch.object(boto3, "client", _client)

    awss = AWSSource("path", test_param="test")

    assert awss.path == "path"
    assert awss.ssm == {
        "service": "ssm",
        "region": "us-east-1",
        "test_param": "test",
    }


def test_to_dict(mocker):
    import boto3

    fake_ssm = mocker.MagicMock()

    def _client(*_, **__):
        return fake_ssm

    mocker.patch.object(boto3, "client", _client)

    responses = [
        {
            "Parameters": [{"Name": "/path/a/val", "Value": 1}, {"Name": "/path/a/b/c", "Value": "c"}],
            "NextToken": "yes",
        },
        {
            "Parameters": [
                {"Name": "/path/a/b/d", "Value": "d"},
                {"Name": "/path/e", "Value": 4},
                {"Name": "/path/list", "Value": "[1,2,3]"},
                {"Name": "/path/dict", "Value": '{"a":1, "b":2}'},
            ]
        },
    ]
    iterator = iter(responses)

    def _get(*_, **__):
        return next(iterator)

    fake_ssm.get_parameters_by_path = _get

    awss = AWSSource("path")

    assert awss.to_dict() == {
        "a": {"b": {"c": "c", "d": "d"}, "val": 1},
        "e": 4,
        "list": [1, 2, 3],
        "dict": {"a": 1, "b": 2},
    }


def test_items(mocker):
    import boto3

    mocker.patch.object(boto3, "client")
    awss = AWSSource("path")

    to_dict_return = {1: 2, 3: 4, 5: 6}
    to_dict = mocker.patch.object(awss, "to_dict", return_value=to_dict_return)

    assert awss.items() == to_dict_return.items()
    to_dict.assert_called_once()
