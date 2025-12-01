from django import template

register = template.Library()

@register.filter
def intdot(value):
    """Convierte 1000000 → 1.000.000"""
    try:
        valor = int(value)
        return f"{valor:,}".replace(",", ".")
    except:
        return value
