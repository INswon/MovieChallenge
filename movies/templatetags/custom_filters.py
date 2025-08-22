from django import template

register = template.Library()

@register.filter(name="get_item")
def get_item(mapping, key):
    """
    dict からキーで取り出す。見つからなければ空文字。
    """
    try:
        return mapping.get(key, "")
    except AttributeError:
        return ""
