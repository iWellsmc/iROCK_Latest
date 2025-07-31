from custom_auth.models import Companies,Settings,User


def tenant_middleware(get_response):
    def middleware(request):
        if request.user.is_authenticated:
            try:
                company = Companies.objects.get(pk=request.user.company_id)
            except Companies.DoesNotExist:
                company = None
            # and it to the request
            request.company = company
            
            # all done, the view will receive a request with a tenant attribute
        return get_response(request)

    return middleware



# def user_middleware(get_response):
#     def usermiddleware(request):
#         if request.user.is_authenticated:
#             print("")
#             try:
#                 user = User.objects.get(pk=request.user.id)
#                 print(request.user.id)
#             except User.DoesNotExist:
#                 user = None
#             # and it to the request
#             request.user = user
            
#             # all done, the view will receive a request with a tenant attribute
#         return get_response(request)

#     return usermiddleware

import pytz

from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

class TimezoneMiddleware(MiddlewareMixin):
    def process_request(self, request):
        tzname = request.session.get('companytimezone')
        # print("tzname",tzname)
        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()