"""OpenAPI core contrib falcon middlewares module"""
from functools import wraps

from openapi_core.validation.processors import OpenAPIProcessor


class FalconOpenAPIMiddleware(OpenAPIProcessor):

    def __init__(
            self,
            request_validator,
            response_validator,
            request_factory,
            response_factory,
            request_provider,
            openapi_errors_handler,
    ):
        super(FalconOpenAPIMiddleware, self).__init__(
            request_validator, response_validator)
        self.request_factory = request_factory
        self.response_factory = response_factory
        self.request_provider = request_provider
        self.openapi_errors_handler = openapi_errors_handler

    def process_request(self, req, resp):
        openapi_req = self._get_openapi_request(req)
        req_result = super(FalconOpenAPIMiddleware, self).process_request(
            openapi_req)
        if req_result.errors:
            return self._handle_request_errors(req_result)
        req.openapi = req_result

    def process_response(self, req, resp, resource, req_succeeded):
        openapi_req = self._get_openapi_request(req)
        openapi_resp = self._get_openapi_response(resp)
        resp_result = super(FalconOpenAPIMiddleware, self).process_response(
            openapi_req, openapi_resp)
        if resp_result.errors:
            return self._handle_response_errors(resp_result)

    def _handle_request_errors(self, request_result):
        return self.openapi_errors_handler.handle(request_result.errors)

    def _handle_response_errors(self, response_result):
        return self.openapi_errors_handler.handle(response_result.errors)

    def _get_openapi_request(self, request):
        return self.request_factory.create(request)

    def _get_openapi_response(self, response):
        return self.response_factory.create(response)
