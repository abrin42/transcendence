from django.utils.deprecation import MiddlewareMixin

class ContentSecurityPolicyMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        csp_header = (
            "default-src 'self'; "
            "script-src 'self'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data:; "
            "object-src 'none';"
        )
        response['Content-Security-Policy'] = csp_header
        return response
