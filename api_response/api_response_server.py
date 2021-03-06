from django.apps import apps as dj_apps
from django.core import serializers
from .json_responses import ApiDefaultResponses
from .snippets import validate_response_length
import json
from .api_app_settings import (
    RESPONSE_LENGTH,
    GET_FULL_RESPONSE,
    DEBUG
)

RESPONSE_LENGTH = validate_response_length(RESPONSE_LENGTH, GET_FULL_RESPONSE)

class ResponseServer:
    def __init__(self):
        pass

    def get_response(self, app_label, model_name, params):
        model = dj_apps.get_model(app_label, model_name=model_name)

        if params:
            queryset = model.objects.filter(**params)
            return self.query_database(queryset)

        else:
            queryset = model.objects.all().order_by('-id')[:RESPONSE_LENGTH]
            response = self.query_database(queryset)
            additional_info = ApiDefaultResponses.APP_ENDPOINT['info']
            if DEBUG:
                additional_info = ApiDefaultResponses.APP_ENDPOINT_DEBUG['info']

            response += additional_info
            return response

    def query_database(self, queryset):
        _data = []
        if queryset:
            for each in queryset:
                temp_dic = {}
                raw_data = serializers.serialize('json', [each])
                response = json.loads(raw_data)[0]
                temp_dic['id'] = response['pk']
                temp_dic.update(response['fields'])
                _data.append(temp_dic)
        return _data
