from django.core.paginator import Paginator


class ListObjectsMixin:

    @staticmethod
    def get_paginated_response(request, objects):
        page_number = request.GET.get('page_number', '1')
        page_size = request.GET.get('page_size', '10')
        page_number = int(page_number) if page_number.isdigit() else 1
        page_size = int(page_size) if page_size.isdigit() else 10

        paginator = Paginator(objects, page_size)
        pages_count = paginator.num_pages

        items = paginator.get_page(page_number).object_list

        return dict(
            items_count=len(objects),
            pages_count=pages_count,
            current_page=page_number,
            items=items
        )
