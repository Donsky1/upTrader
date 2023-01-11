from django import template

from app_menu.models import TreeMenu

register = template.Library()


@register.inclusion_tag('app_menu/menu_template.html', takes_context=True)
def draw_menu(context, name_menu):
    active_menu = context['request'].path
    structure_menu = {}
    parent_id = None
    active_menu_id = None
    item_menu = TreeMenu.objects.filter(global_parent__name=name_menu). \
        select_related('parent', 'global_parent').order_by('parent')

    for item in item_menu:
        # get ids for show unwrapped menu
        if item.get_absolute_url() == active_menu:
            parent_id = item.get_parent_id()
            active_menu_id = item.id

        # create dict menu
        # if not parent element
        if not item.parent:
            structure_menu[item] = []
        else:
            # if item have parent field, finding in
            # structure_menu keys
            for k, v in structure_menu.items():
                if item.parent == k:
                    structure_menu[k].append(item)
                    break
                # structure_menu values
                if item.parent in v:
                    index = structure_menu[k].index(item.parent)
                    structure_menu[k][index] = {item.parent: [item]}
                    break
                # structure_menu values if values have dict element
                for sub_menu in v:
                    if isinstance(sub_menu, dict) and item.parent == list(sub_menu.keys())[0]:
                        sub_menu[item.parent].append(item)
                        break
    return {'menu_dict': structure_menu, 'parent_id': parent_id, 'active_menu_id': active_menu_id}


@register.filter
def get_key_from_dict(value):
    if isinstance(value, dict):
        return list(value.keys())[0]
    else:
        return value


@register.filter
def get_values_from_dict(value):
    if isinstance(value, dict):
        return list(value.values())[0]
    else:
        return value
