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
    data = {"status":0}
    data = json.dumps(data)
    return HttpResponse(data,content_type= 'application/json')
