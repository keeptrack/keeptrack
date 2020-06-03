import datetime
from django import template
register = template.Library()

def add_default(ctx, arg, default, kwargs):
    if arg in kwargs:
        ctx[arg] = kwargs[arg]
    else:
        ctx[arg] = default

@register.inclusion_tag('keeptrack_hire/form_field.html')
def form_field(value, *args, **kwargs):
    ctx = {
        'id': kwargs['id'],
        'name': kwargs['name'],
        'value': value
    }

    add_default(ctx, 'editable', False, kwargs)
    add_default(ctx, 'size', 'col-sm', kwargs)
    add_default(ctx, 'type', 'text', kwargs)

    if 'tooltip' in kwargs:
        ctx['tooltip'] = kwargs['tooltip']

    if 'style' in kwargs:
        ctx['style'] = kwargs['style']

    return ctx

@register.filter(name='eactivities_csp_text')
def eactivities_csp_text(value):
    if value == "" or value == None:
        return '--'

    return f'[{value.zfill(3)}] Society name here'
