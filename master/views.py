import json
import logging
import traceback
from django.http.response import HttpResponse, JsonResponse
import requests
from main import Routes
import io
import os
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
    if request.method == 'GET':
        input_time = request.GET.get('datetime','07.01.2018 09:04:42')
        input_stop = request.GET.get('neareststop','turkman gate')
        input_final_stop = request.GET.get('finalstop','ganesh nagar')
        number_of_buses = 1
        print("input_time ="+str(input_time)+ "&input_stop ="+input_stop + "&input_final_stop ="+input_final_stop)

        obj = Routes(input_time, input_stop, input_final_stop, number_of_buses)
        print("obj ="+str(obj))
        variables = obj.validate_variables()    
        print("variables ="+str(variables))
        result_data = obj.get_route_information(variables)
        print("result_data ="+str(result_data))

        data = {"status":1, 
                "datetime" : input_time, 
                "neareststop" : input_stop, 
                "finalstop" : input_final_stop,
                }
        data = json.dumps(data)
        return HttpResponse(data,content_type= 'application/json')
    data = {"status":0}
    return HttpResponse(data,content_type= 'application/json')


def set_bus_location(request):
    if request.method == 'GET':
        lat = request.GET.get('lat','')
        lng = request.GET.get('lng','')
        print('lat '+str(lat) + ' & lng '+str(lng))
        data = {"lat" : lat, "lng" : lng}
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, 'busData.json')
        print("file_path ="+file_path)
        with open(file_path, 'w') as outfile:
            json.dump(data, outfile)
        sendData = {'status':'success'}
        return HttpResponse(data,content_type= 'application/json')


def get_bus_location(request):
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, 'busData.json')
    with open(file_path, "r") as jsonFile:
        data = json.load(jsonFile)
        lat = data['lat']
        lng = data['lng']
        responseData = {'lat' : lat, 'lng' : lng}
        return JsonResponse(responseData)


