from django import template
from django.urls import reverse
from django.template import Variable, TemplateSyntaxError
from django.contrib.auth.models import Group
from django.forms.models import model_to_dict
from django.utils.safestring import mark_safe
from django.core import serializers

register = template.Library()


@register.simple_tag
def active_url(request, url_name, **kwargs):
    """
    Returns a class to be assiged CSS styling that should make the chosen
    element highlighted as responsible of being in the active url.

    Usage: Assuming that the reversed url is the current url, this tag will act
    as follows:

    {% active_url request url_name %} -> class="ui-active-url"
    {% active_url request url_name class_name=myclass %} -> class="myclass"
    {% active_url request url_name use_class=False %} -> ui-active-url
    {% active_url request url_name class_name=myclass use_class=False %} -> myclass

    Where "urlname" is the name of the url to check;
    this must be defined in your `URLCONF`, otherwise it will raise
    a NoReverseMatch Error.
    """
    class_name = kwargs.get('class_name', 'ui-active-url')
    use_class = kwargs.get('use_attr', True)

    url = reverse(url_name)
    if request.path == url:
        return (class_name, ' class="%s"' % class_name)[use_class]
    return ''


@register.simple_tag
def current_url(request, url_name):
    """
    Returns the reversed url only if it is NOT the current url.
    Otherwise returns the character "`#`"

    Usage:
    <a href="{% current_url request url_name %}">Some link</a>
    """
    url = reverse(url_name)
    if request.path == url:
        return '#'
    return url


@register.tag()
def ifmember(parser, token):
    """
    Checks if the current user belongs to a specific group.

    - User must be looged in.
    - Requires the Django authentication contrib app and middleware.

    Usage: {% ifmember Admins %} ... {% endifusergroup %}
    """
    try:
        tag, group = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError("Tag 'ifmember' requires 1 argument.")
    nodelist = parser.parse(('endifmember',))
    parser.delete_first_token()
    return GroupCheckNode(group, nodelist)


class GroupCheckNode(template.Node):
    def __init__(self, group, nodelist):
        self.group = group
        self.nodelist = nodelist

    def render(self, context):
        user = Variable('user').resolve(context)
        if not user.is_authenticated:
            return ''
        try:
            group = Group.objects.get(name=self.group)
        except Group.DoesNotExist:
            return ''
        if group in user.groups.all():
            return self.nodelist.render(context)
        return ''


@register.tag
def mkrange(parser, token):
    """
    Accepts the same arguments as the 'range' builtin and creates
    a list containing the result of 'range'.

    Usage:
        {% mkrange [start, ]stop[, step] as context_name %}

    For example:
        {% mkrange 5 10 2 as some_range %}
        {% for i in some_range %}
          {{ i }}: Something I want to repeat
        {% endfor %}

    Produces:
        5: Something I want to repeat
        7: Something I want to repeat
        9: Something I want to repeat
    """

    tokens = token.split_contents()
    fnctl = tokens.pop(0)

    def raise_error():
        raise TemplateSyntaxError('%s accepts the syntax: {%% %s [start,] ' +
                                  'stop[, step] as context_name %%}, where "start", "stop" ' +
                                  'and "step" must all be integers.' % (fnctl, fnctl))

    range_args = []

    while True:
        if len(tokens) < 2:
            raise_error()
        token = tokens.pop(0)
        if token == "as":
            break
        if not token.isdigit():
            raise_error()
        range_args.append(int(token))

    if len(tokens) != 1:
        raise_error()

    context_name = tokens.pop()

    return RangeNode(range_args, context_name)


class RangeNode(template.Node):
    def __init__(self, range_args, context_name):
        self.range_args = range_args
        self.context_name = context_name

    def render(self, context):
        context[self.context_name] = range(*self.range_args)
        return ''


# Model helpers
@register.simple_tag
def get_model_as_dict(instance):
    """
    Returns a django model instance as dictionary

    Usage: {% get_model_as_dict model_instance %}
    """
    return model_to_dict(instance)


@register.simple_tag
def get_verbose_field_name(instance, field_name):
    """
    Returns the name title of a django field model instance

    Usage: {% get_verbose_field_name model_instance model_field %}
    """
    return instance._meta.get_field(field_name).verbose_name.title()


@register.simple_tag
def get_modelfield_url(field):
    """
    Returns url of filefield or imagefield object

    Usage: {% get_field_url model_instance.model_field %}
    """
    """Regresa el field url de un FileField o ImageField """
    return field.url


@register.simple_tag
def serialize_queryset(queryset, fields=None):
    """
    Returns queryset, with filtered fields if included

    Usage: {% serialize_queryset queryset %}
    """
    if fields:
        return serializers.serialize("python", queryset, fields=tuple(fields.split(",")))
    return serializers.serialize("python", queryset)


# General helpers
@register.simple_tag
def sorted_dict_fields(dict, fields):
    """
    Returns sorted dict based on list

    Usage: {% sorted_dict_fields dict %}
    """
    ordered_fields = fields.split(",")
    new_dict = {k: v for k, v in dict.items() if k in ordered_fields}
    return sorted(new_dict.items(), key=lambda pair: ordered_fields.index(pair[0]))


@register.simple_tag
def template_dir(this_object):
    """
    Returns dir of object for introspection

    Usage: {% template_dir object %}
    """
    return mark_safe("<pre>" + str(dir(this_object)) + "</pre>")
