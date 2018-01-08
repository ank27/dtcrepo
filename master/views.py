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
    datetime = request.POST.get("datetime")
    neareststop = request.POST.get("neareststop")
    finalstop = request.POST.get("finalstop")

    datetime1 = request.POST["datetime"]
    neareststop1 = request.POST["neareststop"]
    finalstop1 = request.POST["finalstop"]

    data = {"status":1, "datetime" : datetime, "neareststop" : neareststop, "finalstop" : finalstop,
            "datetime1" : datetime1, "neareststop1" : neareststop1, "finalstop1" : finalstop1}
    data = json.dumps(data)
    return HttpResponse(data,content_type= 'application/json')