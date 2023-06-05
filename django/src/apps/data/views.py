import json
from datetime import datetime, date

from django.shortcuts import render

from apps.data.models import Lake


# Create your views here.


def json_default(value):
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    else:
        return value.__dict__


def store_in_lake(origin: str, ref: dict, raw: object):
    lake = Lake.objects.create(
        origin=origin, ref=ref, raw=raw if isinstance(raw, dict) else json.dumps(raw, default=json_default)
    )
