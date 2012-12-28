from django import template
from django.template import resolve_variable, TemplateSyntaxError
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse

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
        user = resolve_variable('user', context)
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
        raise TemplateSyntaxError('%s accepts the syntax: {%% %s [start,] ' + \
            'stop[, step] as context_name %%}, where "start", "stop" ' + \
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
