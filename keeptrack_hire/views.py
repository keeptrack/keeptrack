import datetime
import json

from django.views import generic, View
from django.shortcuts import get_object_or_404, render, reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404, QueryDict

from equipment.models import Asset
from hire.models import HireRequest
from .models import AllocatedEquipment, AllocatedCustomItems

def delete_hire(request, **kwargs):
    key = kwargs['pk']
    obj = HireRequest.objects.get(pk=key)
    return HttpResponse(f"Deleting element {key}: {obj}")

class IndexView(generic.ListView):
    model = HireRequest
    ordering = ['-hire_from']

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context

class HireView(View):
    template_name = 'keeptrack_hire/edit_hire.html'

    def get(self, request, *args, **kwargs):
        hire = get_object_or_404(HireRequest, pk=kwargs['pk'])
        disabled = 'readonly' if 'edit' not in request.GET else ''

        ctx = {
            'hire': hire,
            'disabled': disabled,
            'duration': (hire.hire_to - hire.hire_from).days + 1
        }

        allocated_assets = AllocatedEquipment.objects.filter(request=hire)
        if allocated_assets.exists():
            ctx['allocated_assets'] = allocated_assets

        allocated_custom_items = AllocatedCustomItems.objects.filter(request=hire)
        if allocated_custom_items.exists():
            ctx['custom_items'] = allocated_custom_items

        return render(request, self.template_name, ctx)

    def _sanitize_soc_string(self, cspId):
        if cspId == '--' or not cspId.isnumeric():
            return ""
        return int(cspId)

    def post(self, request, *args, **kwargs):
        print(request.POST)

        def get_post_or_404(arg):
            if arg not in request.POST:
                raise Http404(f"Did not submit POST parameter {arg}")
            return request.POST.get(arg)

        to_date = lambda str: datetime.datetime.strptime(str, '%Y-%m-%d').date()

        item = get_object_or_404(HireRequest, pk=kwargs['pk'])

        # Override items from request
        item.name = get_post_or_404('hire-name')
        item.email = get_post_or_404('hire-email')
        item.cid = get_post_or_404('hire-cid')
        item.hire_from = to_date(get_post_or_404('hire-from'))
        item.hire_to = to_date(get_post_or_404('hire-to'))

        # TODO: Figure out why DB doesn't update this field.
        item.description = get_post_or_404('hire-desc')

        item.save()

        return HttpResponseRedirect(reverse('keeptrack_hire:edit_hire', kwargs={'pk':item.id}))

#region Approval status change

def _set_flags_and_redirect(key, approved, rejected):
    obj = get_object_or_404(HireRequest, pk=key)
    obj.approved = approved
    obj.rejected = rejected
    obj.save()

    return HttpResponseRedirect(reverse('keeptrack_hire:edit_hire', kwargs={'pk':key}))

def approve_hire(request, **kwargs):
    key = kwargs['pk']
    return _set_flags_and_redirect(key, True, False)

def reject_hire(request, **kwargs):
    key = kwargs['pk']
    return _set_flags_and_redirect(key, False, True)

def unmark_hire(reqiest, **kwargs):
    key = kwargs['pk']
    return _set_flags_and_redirect(key, False, False)

#endregion

#region Adding and removing items from equipment list

class UpdateAssetsView(View):
    def get(self):
        return HttpResponse()

    def _float_or_none(self, str):
        try:
            return float(str)
        except ValueError:
            return None

    def put(self, request, **kwargs):
        hire_id = kwargs['pk']
        hire = get_object_or_404(HireRequest, pk=hire_id)

        data = QueryDict(request.body)
        asset_id = data['asset-id']
        asset_discount_price = self._float_or_none(data['discounted-price'])

        asset = Asset.objects.get(uid=asset_id)
        binding = AllocatedEquipment(request=hire, asset=asset, discounted_price = asset_discount_price)
        print(binding)
        binding.save()

        return HttpResponse()

def remove_asset(request, **kwargs):
    hire = get_object_or_404(HireRequest, pk=kwargs['pk'])
    asset = get_object_or_404(Asset, pk=kwargs['asset'])

    allocation = get_object_or_404(AllocatedEquipment, request=hire, asset=asset)
    allocation.delete()

    return HttpResponseRedirect(reverse('keeptrack_hire:edit_hire', kwargs={'pk':hire.id}))

class UpdateCustomView(View):
    def _float_or_404(self, str):
        try:
            return float(str)
        except ValueError:
            raise Http404

    def put(self, request, **kwargs):
        hire_id = kwargs['pk']
        hire = get_object_or_404(HireRequest, pk=hire_id)

        data = QueryDict(request.body)
        text = data['itemname']
        price = self._float_or_404(data['price'])

        item = AllocatedCustomItems(request=hire, text=text, price=price)
        item.save()

        return HttpResponse()


def remove_custom(request, **kwargs):
    hire = get_object_or_404(HireRequest, pk=kwargs['pk'])

    item = get_object_or_404(AllocatedCustomItems, pk=kwargs['item'])
    item.delete()

    return HttpResponseRedirect(reverse('keeptrack_hire:edit_hire', kwargs={'pk':hire.id}))

#endregion

class AvailableAssetsJsonView(View):
    def _get_free_assets(self, hire):
        # Find all hires that overlap with current hire.
        all_hires = HireRequest.objects             \
            .filter(approved=True)                  \
            .exclude(hire_from__gt=hire.hire_to)    \
            .exclude(hire_to__lt=hire.hire_from)

        # Find all allocated assets associated with these hires.
        allocated_assets = map(lambda hire: AllocatedEquipment.objects.filter(request=hire),
                               all_hires)
        assets = Asset.objects.all()
        for qs in allocated_assets:
            for asset in qs:
                assets = assets.exclude(uid=asset.asset.uid)

        return assets

    def _get_free_assets_as_ctx_list(self, hire, query_text):
        assets = self._get_free_assets(hire)
        return list(map(lambda a: {
            'id': a.uid,
            'category': a.category,
            'brand': a.brand,
            'name': a.name,
            'condition': a.condition
        }, assets))

    def get(self, request, *args, **kwargs):
        hire = get_object_or_404(HireRequest, pk=kwargs['pk'])
        query_text = request.GET.get('q')

        assets = self._get_free_assets_as_ctx_list(hire, query_text)

        return HttpResponse(json.dumps(assets), content_type="application/json")
