import json
import logging
import traceback
from django.http.response import HttpResponse
import requests

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
    print("get bus status called")
    datetime = requests.POST.get("datetime","")
    neareststop = requests.POST.get("neareststop","")
    finalstop = requests.POST.get("finalstop","")
    print 'datetime ='+str(datetime)
    data = {"status":1, 
            "datetime" : datetime, 
            "neareststop" : neareststop, 
            "finalstop" : finalstop,
            }
    data = json.dumps(data)
    return HttpResponse(data,content_type= 'application/json')