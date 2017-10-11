import json
from copy import deepcopy
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.views.generic.list import BaseListView
from .models import Category, Order

STANDARD_RESPONSE = {
    'data': [],
    'message': ''
}
AUTH_FAIL_MESSAGE = 'Access denied. You are not authenticated (access /o/token) ' \
                    'or not authorized (contact administration)'


class JSONResponseMixin(object):
    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(self.get_data(context),
                            status=context.get('status', 200),
                            **response_kwargs)

    def get_data(self, context):
        raise NotImplementedError


class CategoriesListView(BaseListView, JSONResponseMixin):
    queryset = Category.objects.filter(parent__id=None)
    model = Category

    def get_data(self, context):
        lst = deepcopy(STANDARD_RESPONSE)
        # Checking perm here not to dive into
        # how to return JsonResponse from PermissionDenied handler
        if not self.request.user.has_perm('api.view_categories'):
            lst['message'] = AUTH_FAIL_MESSAGE
            context['status'] = 403
        else:
            lst['message'] = 'Success'
            context['status'] = 200
            for category in self.get_queryset():
                lst['data'].append(category.get_dict())
        return lst


@method_decorator(csrf_exempt, name='dispatch')
class OrdersCreateView(View):
    def post(self, request, *args, **kwargs):
        data = deepcopy(STANDARD_RESPONSE)
        if 'json' not in self.request.content_type.lower():
            data.update({'message': 'Wrong content type: should be like \'application/json\''})
            return JsonResponse(data, status=415)
        if not self.request.user.has_perm('api.create_orders'):
            data.update({'message': AUTH_FAIL_MESSAGE})
            return JsonResponse(data, status=403)
        try:
            payload = json.loads(self.request.body)
        except:
            data.update({'message': 'Errors in JSON'})
            return JsonResponse(data, status=400)
        created_order = Order.create_from_payload(payload, self.request.user)
        status = 201
        if created_order:
            data.update({
                'data': created_order.get_dict(),
                'message': 'Success'
            })
        else:
            data.update({'message': 'Failed to create new order'})
            status = 400
        return JsonResponse(data, status=status)