from collections import OrderedDict

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class LimitedOffsetPaginator(LimitOffsetPagination):
    """
    Paginator that "works" with large querysets of heavy instances by truncating
    them into manageable size.
    """
    default_limit = 20
    truncate_size = 1000
    truncated = False

    def paginate_queryset(self, queryset, request, view=None):
        self.limit = self.get_limit(request)
        if self.limit is None:
            return None

        self.offset = self.get_offset(request)
        self.count = queryset.count()
        # Truncate if too large, don't overload the DB
        if self.count > self.truncate_size:
            self.count = self.truncate_size
            self.truncated = True

        self.request = request
        if self.count > self.limit and self.template is not None:
            self.display_page_controls = True

        if self.count == 0 or self.offset > self.count:
            return []
        return list(queryset[self.offset:self.offset + self.limit])

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data),
            ('truncated', self.truncated),
        ]))
