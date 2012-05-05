import locale
import re
from datetime import date
from django import template
from django.template.defaultfilters import stringfilter
from django.forms.fields import (
    CharField,
    TypedChoiceField,
    DecimalField,
    IntegerField,
    BooleanField,
    NullBooleanField,
    DateField,
    DateTimeField,
)

register = template.Library()


@register.filter()
def currency(value, other_locale=None):
    """
    Returns value represented as currency for the give locale.

    Usage::
    {{ value|currency }}

    For example:
    Assuming value is 13, {{ value|currency }}

    Produces:
    $13.00
    """
    if type(value) in (int, float):
        locale.setlocale(locale.LC_ALL, '%s.utf8' % (other_locale or 'en_US'))
        return locale.currency(value, grouping=True)
    return value


@register.filter
def int(value):
    """
    Returns the given value as an int type.

    Usage::
    {{ value|int }}
    {% tag_that_requires_int value|int %}
    """
    try:
        return int(value)
    except ValueError:
        return value


@register.filter
def nolinebrs(value):
    """
    Removes all <br> tags in the given string.
    """
    return re.sub('<br\s*\/?>', '', value)


@register.filter
@stringfilter
def startswith(value, arg):
    """
    Returns whether the given value starts with the given string arg.
    <arg> must be a string
    """
    return value.startswith(arg)


@register.filter
def creditcard(value, arg):
    """
    Hides parts of strings such as credit card or bank account numbers to
    show only the last amount of numbers.

    Usage: {{ value|creditcard:4 }}

    For example:
    Assuming value is "5000000000003456"
    {{ value|creditcard:4 }}

    Produces:
    ************3456
    """
    return '*' * len(value[:-arg]) + value[-arg:]


@register.filter(name='display')
def get_display_value(bound_field, default=None):
    """
    Returns the verbose value of a ChoiceField.

    Usage:
    {{ form.field|display }}

    or

    {% for field in form %}
        {{ field|display }}
    {% endfor %}

    For example:
    Assuming <field> is a BooleanField with True
    {{ field|display }}

    Produces: The string 'Yes'
    """
    NO_DATA_MESSAGE = 'Not Available'
    if default:
        NO_DATA_MESSAGE = default

    field_type = type(bound_field.field)
    # For text and numeric types, return the plain value
    if isinstance(field_type, (CharField, DecimalField, IntegerField)):
        return bound_field.value() if bound_field.value() else NO_DATA_MESSAGE
    # For boolean type, return a verbose representation of the value
    elif isinstance(field_type, (BooleanField, NullBooleanField)):
        if bound_field.value() is None:
            return default or 'Maybe'
        return ('No', 'Yes')[bound_field.value()]
    # For choices, return the verbose value
    elif isinstance(field_type, TypedChoiceField):
        return dict(field_type.choices).get(bound_field.value(), NO_DATA_MESSAGE)
    # For date types, return the age until the current date.
    if isinstance(bound_field.field, (DateField, DateTimeField)):
        age = (date.today() - bound_field.value()).days / 365
        return age
