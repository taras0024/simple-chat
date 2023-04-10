from collections import OrderedDict

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class WebLimitOffsetPagination(LimitOffsetPagination):
    max_limit = 20

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.count),
            ('next', OrderedDict([('offset', self.offset + self.limit), ('limit', self.limit)])),
            ('previous', OrderedDict([('offset', max(self.offset - self.limit, 0)), ('limit', self.limit)])),
            ('results', data)
        ]))

    def get_paginated_response_schema(self, schema):
        return {
            'type': 'object',
            'properties': {
                'count': {
                    'type': 'integer',
                    'example': 123,
                },
                'next': {
                    'type': 'object',
                    'properties': {
                        'offset': {
                            'type': 'integer',
                            'example': 400,
                        },
                        'limit': {
                            'type': 'integer',
                            'example': 100,
                            'default': self.default_limit,
                            'maximum': self.max_limit,
                        }
                    },
                },
                'previous': {
                    'type': 'object',
                    'properties': {
                        'offset': {
                            'type': 'integer',
                            'example': 200,
                        },
                        'limit': {
                            'type': 'integer',
                            'example': 100,
                            'default': self.default_limit,
                            'maximum': self.max_limit,
                        }
                    }
                },
                'results': schema,
            },
        }
