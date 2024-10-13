from packages.serializers import PackageSerializer

def test_package_serializer():
    data = {
        'name': 'example-package',
        'version': '1.0.0',
        'dependencies': []
    }
    serializer = PackageSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.validated_data == data