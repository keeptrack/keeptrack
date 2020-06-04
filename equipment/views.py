from django.shortcuts import render
from equipment.models import Asset


# Create your views here.
def index(request):
    assets = Asset.objects.all()
    last_uid = 1

    for asset in assets:
        if asset.uid > last_uid:
            last_uid = asset.uid

    return render(request, "equipment/index.html", {
        "last_uid": last_uid,
        "equipment_list": map(Asset.to_dict, assets)
    })
