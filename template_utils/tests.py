from decimal import Decimal
from django import forms
from django.test import TestCase
from django.template import Template, Context
from django.utils import timezone
from django.utils.timezone import utc
from template_utils.templatetags import templateutils_filters


class MyForm(forms.Form):
    FORM_CHOICES = (
        ('foo', 'FOO'),
        ('bar', 'BAR'),
        ('baz', 'BAZ')
    )
    char = forms.CharField(max_length=3)
    decimal_ = forms.DecimalField()
    integer = forms.IntegerField()
    boolean = forms.BooleanField()
    null_boolean = forms.NullBooleanField()
    choice = forms.TypedChoiceField(choices=FORM_CHOICES)
    date = forms.DateField()
    datetime = forms.DateTimeField()


class TemplateWithFilter(object):
    def __init__(self):
        self.value = None
        self.filter = None
        self.filter_arg = None
        self.result = None

    def render(self, value, filter_, arg=None):
        """ Renders the value for the given filter. """
        self.value = value
        self.filter = filter_
        self.filter_arg = (':"%s"' % arg) if arg else ''

        # Render the value using the filter
        render_value_str = '{{ value|%s%s }}' % (self.filter, self.filter_arg)
        tpl = Template('{% load templateutils_filters %}' + render_value_str)
        c = Context({'value': self.value})
        template_result = tpl.render(c)

        # Process the value with the raw filter
        f = getattr(templateutils_filters, self.filter)
        args = [value] if not arg else [value, arg]
        filter_result = f(*args)

        self.results = {
            'template': template_result,
            'filter': filter_result
        }

    def equals(self, expected):
        """ Asserts that the produced value is the same as the expected. """
        match = self.results['filter'] == expected and \
            self.results['template'] == unicode(expected)
        return match


class TemplateFiltersTest(TestCase):
    def setUp(self):
        self.text = TemplateWithFilter()

    def test_currency(self):
        self.text.render(12, 'currency')  # test with int
        # assert self.text.equals('$12.00')
        self.text.render(12.505, 'currency')  # test with float
        assert self.text.equals('$12.51')
        self.text.render(Decimal('12.505'), 'currency')  # test with decimal
        assert self.text.equals('$12.51')

    def test_integer(self):
        self.text.render(1.5, 'integer')
        assert self.text.equals(1)

    def test_nolinebrs(self):
        value = """
        Lorem ipsum dolor sit amet, consectetur adipisicing elit,<br />
        sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.<br/>
        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris<br>
        nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor
        """
        expected = """
        Lorem ipsum dolor sit amet, consectetur adipisicing elit,
        sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris
        nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor
        """
        self.text.render(value, 'nolinebrs')
        assert self.text.equals(expected)

    def test_startswith(self):
        value = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit,'
        self.text.render(value, 'startswith', arg='Lorem')
        assert self.text.equals(True)
        self.text.render(value, 'startswith', arg='not found')
        assert self.text.equals(False)

    def test_creditcard(self):
        value = '370000000000002'
        expected_3 = '************002'
        expected_4 = '***********0002'
        self.text.render(value, 'creditcard')
        assert self.text.equals(expected_4)
        self.text.render(value, 'creditcard', 3)
        assert self.text.equals(expected_3)


class DisplayFieldFilterTest(TestCase):
    SOME_BIRTHDATE = timezone.datetime(1989, 7, 27, 3, 2, tzinfo=utc)
    NOW = timezone.now()

    def setUp(self):
        self.text = TemplateWithFilter()
        self.form = MyForm(initial={
            'char': 'foo',
            'decimal_': Decimal(10),
            'integer': 11,
            'boolean': True,
            'null_boolean': None,
            'date': self.SOME_BIRTHDATE.date(),
            'datetime': self.SOME_BIRTHDATE,
            'choice': 'bar'
        })

    def get_display_value(self, field, expected_value):
        self.text.render(field, 'verbose')
        assert self.text.equals(expected_value)

    def test_get_display(self):
        EXPECTED_AGE = (self.NOW - self.SOME_BIRTHDATE).days / 365
        self.get_display_value(self.form['char'], 'foo')
        self.get_display_value(self.form['decimal_'], Decimal(10))
        self.get_display_value(self.form['integer'], 11)
        self.get_display_value(self.form['boolean'], 'Yes')
        self.get_display_value(self.form['null_boolean'], 'Maybe')
        self.get_display_value(self.form['date'], EXPECTED_AGE)
        self.get_display_value(self.form['datetime'], EXPECTED_AGE)
        self.get_display_value(self.form['choice'], 'BAR')
