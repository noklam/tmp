from rest_framework import renderers
from adrf import views
from rest_framework.request import Request
from rest_framework.response import Response

from packages.modules import npm
from packages.serializers import PackageSerializer


class PackageView(views.APIView):
    renderer_classes = [renderers.JSONRenderer]

    async def get(self, request: Request, package_name: str, range: str | None = None):

        if range is None:
            range = "*"
        package_info = await npm.get_package_with_transitive_dependencies(package_name, range)
        serializer = PackageSerializer(package_info)
        return Response(serializer.data)
