from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, "equipment/index.html", {
        "last_uid": 2,
        "equipment_list": [
            {
                "uid": 1,
                "category": "Camera",
                "brand": "Canon",
                "name": "9000",
                "condition": "Good",
                "value": "2000",
                "storage_location": "Cupboard",
                "next_hire_date": "31 July",
                "hire_price": "10",
                "notes": ""
            },
            {
                "uid": 2,
                "category": "Test",
                "brand": "Test Brand",
                "name": "Test Model",
                "condition": "Out of Order",
                "value": "100",
                "storage_location": "John's house",
                "next_hire_date": "None",
                "hire_price": "20",
                "notes": ""
            }
        ]
    }
    )
