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
