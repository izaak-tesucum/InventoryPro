from django import template

register = template.Library()

@register.filter(name="currency")
def currency(value):
    """Format value as currency"""
    return f"${value:,.2f}"
