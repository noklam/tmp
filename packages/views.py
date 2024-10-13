from adrf import views
from django.http import Http404
from rest_framework import renderers
from rest_framework.request import Request
from rest_framework.response import Response

from packages.modules import npm
from packages.serializers import PackageSerializer


class PackageView(views.APIView):
    renderer_classes = [renderers.JSONRenderer]

    async def get(self, request: Request, package_name: str, range: str | None = None):
        if range is None:
            range = "*"
        try:
            package_info = await npm.get_package_with_transitive_dependencies(
                package_name, range
            )
            serializer = PackageSerializer(package_info)
            return Response(serializer.data)
        except Exception as e:
            return Response(f"{package_name} version not found: {range}")
