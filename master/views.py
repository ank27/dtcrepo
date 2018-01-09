import json
import logging
import traceback
from django.http.response import HttpResponse
import requests
from main import Routes
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
    input_time = request.POST.get('datetime','07.01.2018 09:04:42')
    input_stop = request.POST.get('neareststop','turkman gate')
    input_final_stop = request.POST.get('finalstop','ganesh nagar')
    number_of_buses = 1
    # print 'datetime ='+str(request.POST['datetime'])
    # print 'datetime old ='+str(datetime)

    obj = Routes(input_time, input_stop, input_final_stop, number_of_buses)
    variables = obj.validate_variables()    
    result_data = obj.get_route_information(variables)
    print("result_data ="+result_data)

    data = {"status":1, 
            "datetime" : input_time, 
            "neareststop" : input_stop, 
            "finalstop" : input_final_stop,
            }
    data = json.dumps(data)
    return HttpResponse(data,content_type= 'application/json')


def set_bus_location(request):
    lat = request.POST.get('lat','')
    lng = request.POST.get('lng','')
    print('lat '+str(lat) + ' & lng '+str(lng))
    data = {'lat':lat,
            'lng':lng}
    with open("bus_location.json", "w") as jsonFile:
        json.dump(data, jsonFile)
    sendData = {'status':'success'}
    return HttpResponse(data,content_type= 'application/json')

def get_bus_location(request):
    with open("replayScript.json", "r") as jsonFile:
        data = json.load(jsonFile)
        return HttpResponse(data, content_type='application/json')


