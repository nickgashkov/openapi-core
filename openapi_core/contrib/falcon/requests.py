"""OpenAPI core contrib falcon responses module"""
from json import dumps
import re

from six.moves.urllib.parse import urljoin
from werkzeug.datastructures import ImmutableMultiDict

from openapi_core.validation.request.datatypes import OpenAPIRequest, RequestParameters

# https://falcon.readthedocs.io/en/stable/api/routing.html#field-converters
PATH_PARAMETER_PATTERN = r'{(\w+)(?::(?:int|uuid|dt))?}'


class FalconOpenAPIRequestFactory:

    path_regex = re.compile(PATH_PARAMETER_PATTERN)

    @classmethod
    def create(cls, req, route_params):
        """
        Create OpenAPIRequest from falcon Request and route params.
        """
        method = req.method.lower()

        # Convert keys to lowercase as that's what the OpenAPIRequest expects.
        headers = {key.lower(): value for key, value in req.headers.items()}

        if req.uri_template is None:
            path_pattern = req.path
        else:
            path_pattern = cls.path_regex.sub(r'{\1}', req.uri_template)

        # Support falcon-jsonify.
        body = (
            dumps(req.json) if getattr(req, "json", None)
            else req.bounded_stream.read()
        )
        mimetype = req.options.default_media_type
        if req.content_type:
            mimetype = req.content_type.partition(";")[0]

        parameters = RequestParameters(
            path=route_params,
            query=ImmutableMultiDict(req.params.items()),
            header=headers,
            cookie=req.cookies,
        )
        full_url_pattern = urljoin(req.prefix, path_pattern)
        return OpenAPIRequest(
            full_url_pattern=full_url_pattern,
            method=method,
            parameters=parameters,
            body=body,
            mimetype=mimetype,
        )
