"""OpenAPI core contrib falcon responses module"""
from openapi_core.validation.response.datatypes import OpenAPIResponse


class FalconOpenAPIResponseFactory(object):
    @classmethod
    def create(cls, resp):
        status_code = resp.status[:3]
        mimetype = ''
        if resp.content_type:
            mimetype = resp.content_type.partition(";")[0]
        return OpenAPIResponse(
            data=resp.body,
            status_code=status_code,
            mimetype=mimetype,
        )
