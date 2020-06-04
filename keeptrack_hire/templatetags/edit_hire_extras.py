import datetime
from django import template
register = template.Library()

def add_default(ctx, arg, default, kwargs):
    if arg in kwargs:
        ctx[arg] = kwargs[arg]
    else:
        ctx[arg] = default

@register.inclusion_tag('keeptrack_hire/form_field.html', takes_context=True)
def form_field(context, value, *args, **kwargs):
    out_ctx = {
        'id': kwargs['id'],
        'name': kwargs['name'],
        'value': value,
        'disabled': context['disabled'],
    }

    # Get value of editable from parent context.
    # If it's not present, set it to false.
    add_default(out_ctx, 'size', 'col-sm', kwargs)
    add_default(out_ctx, 'type', 'text', kwargs)

    if 'tooltip' in kwargs:
        out_ctx['tooltip'] = kwargs['tooltip']

    if 'style' in kwargs:
        out_ctx['style'] = kwargs['style']

    return out_ctx

@register.filter(name='eactivities_csp_text')
def eactivities_csp_text(value):
    if value == "" or value == None:
        return '--'

    return f'[{value.zfill(3)}] Society name here'
