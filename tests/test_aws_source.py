from flex_config import AWSSource


class TestAWSSource:
    def test___init__(self, mocker):
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

    def test_items(self, mocker):
        import boto3

        fake_ssm = mocker.MagicMock()

        def _client(*_, **__):
            return fake_ssm

        mocker.patch.object(boto3, "client", _client)

        responses = [
            {"Parameters": [{"Name": "/path/a", "Value": 1}, {"Name": "/path/a/b/c", "Value": 2}], "NextToken": "yes"},
            {"Parameters": [{"Name": "/path/a/b/d", "Value": 3}, {"Name": "/path/e", "Value": 4}]},
        ]
        iterator = iter(responses)

        def _get(*_, **__):
            return next(iterator)

        fake_ssm.get_parameters_by_path = _get

        awss = AWSSource("path")

        results = {}
        for key, value in awss.items():
            results[key] = value

        assert results == {"a": 1, "a/b/c": 2, "a/b/d": 3, "e": 4}
