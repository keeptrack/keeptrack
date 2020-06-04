from django.shortcuts import render
from equipment.models import Asset
from django.http import HttpResponse
import json


# Create your views here.
def index(request):
    assets = Asset.objects.all()
    last_uid = 0

    for asset in assets:
        if asset.uid > last_uid:
            last_uid = asset.uid

    return render(request, "equipment/index.html", {
        "last_uid": last_uid,
        "equipment_list": map(Asset.to_dict, assets)
    })


def update(request):
    try:
        assets = json.loads(request.body)
        for asset in assets:
            action = asset["action"]
            if action == "new":
                asset_obj = Asset(uid=asset["uid"],
                                  category=asset["category"],
                                  brand=asset["brand"],
                                  name=asset["name"],
                                  condition=asset["condition"],
                                  value=asset["value"],
                                  storage_location=asset["storage_location"],
                                  hire_price=asset["hire_price"],
                                  notes=asset["notes"])
                asset_obj.save()
            elif action == "update":
                asset_obj = Asset.objects.filter(uid=asset["uid"])[0]
                asset_obj.category = asset["category"]
                asset_obj.brand = asset["brand"]
                asset_obj.name = asset["name"]
                asset_obj.condition = asset["condition"]
                asset_obj.value = asset["value"]
                asset_obj.storage_location = asset["storage_location"]
                asset_obj.hire_price = asset["hire_price"]
                asset_obj.notes = asset["notes"]
                asset_obj.save()
            elif action == "delete":
                asset_obj = Asset.objects.filter(uid=asset["uid"])[0]
                asset_obj.delete()
    except (json.JSONDecodeError, KeyError):
        response = HttpResponse()
        response.status_code = 400
        return response
    except Exception:
        response = HttpResponse()
        response.status_code = 500
        return response

    return HttpResponse()
