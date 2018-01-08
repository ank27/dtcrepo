import json
import logging
import traceback
from django.http.response import HttpResponse

logger = logging.getLogger(__name__)


def home(request):
    try:
        pass
    except Exception:
        logger.exception("")

    data = {'status': 'Success, Welcome to TSA - DTC Application'}
    data = json.dumps(data)
    return HttpResponse(data, content_type='application/json')


def get_bus_status(request):
    datetime = request.POST.get('datetime')
    neareststop = request.POST.get('neareststop')
    finalstop = request.POST.get('finalstop')

    data = {"status":1, "datetime" : datetime, "neareststop" : neareststop, "finalstop" : finalstop}
    data = json.dumps(data)
    return HttpResponse(data,content_type= 'application/json')