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

    data = {'status': 'success'}
    data = json.dumps(data)
    return HttpResponse(data, content_type='application/json')


def app_status(request):
    data = {"status":1}
    data = json.dumps(data)
    return HttpResponse(data,content_type= 'application/json')

def audio_data(request):
    data = {
        "message": "Success",
        "payload": {
            "id": 1,
            "user": "262f6dc3-4fc6-4c4e-968a-7385d7231421",
            "filename": "audio_files/file_1.wav",
            "created": "2017-04-09T12:23:56.243460"
        },
        "success": True
    }
    data = json.dumps(data)
    return HttpResponse(data, content_type='application/json')
