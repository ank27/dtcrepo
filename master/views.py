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
    datetime = request.POST.get('datetime','')
    neareststop = request.POST.get('neareststop','')
    finalstop = request.POST.get('finalstop','')
    # print 'datetime ='+str(request.POST['datetime'])
    # print 'datetime old ='+str(datetime)
    data = {"status":1, 
            "datetime" : datetime, 
            "neareststop" : neareststop, 
            "finalstop" : finalstop,
            }
    data = json.dumps(data)
    return HttpResponse(data,content_type= 'application/json')

def set_bus_location(request):
    lat = request.POST.get('lat')
    lng = request.POST.get('lng')
    data = {'lat': lat, 'lng' : lng}
    with open("bus_location.json", "w") as jsonFile:
    json.dump(data, jsonFile)

def get_bus_location(request):
    with open("replayScript.json", "r") as jsonFile:
    data = json.load(jsonFile)
    return HttpResponse(data, content_type='application/json')