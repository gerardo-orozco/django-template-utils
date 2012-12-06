# django-template-utils

Just a collection of useful template tags and filters gathered in a single app.

## Usage

### Templatetags

#### active_url

Returns a class to be assiged CSS styling that should make the chosen element highlighted as responsible of being in the active url.

Example: Assuming that the reversed url is the current url, this tag will act as follows:

    {% active_url request url_name %} -> class="ui-active-url"
    {% active_url request url_name class_name=myclass %} -> class="myclass"
    {% active_url request url_name use_class=False %} -> ui-active-url
    {% active_url request url_name class_name=myclass use_class=False %} -> myclass

Where `urlname` is the name of the url to check; this must be defined in your `URLCONF`, otherwise it will raise a `NoReverseMatch` Error.

#### current_url

Returns the reversed url only if it is NOT the current url. Otherwise returns the character "`#`"

Example:

    <a href="{% current_url request url_name %}">Some link</a>

#### ifmember

Checks if the current user belongs to a specific group.

- User must be looged in.
- Requires the Django authentication contrib app and middleware.

Usage:

    {% ifmember Admins %} ... {% endifusergroup %}

#### mkrange

Accepts the same arguments as the builtin `range` function and creates a list containing the result of `range`.

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

### Filters

#### currency

Returns value represented as currency for the give locale.

Usage:

    {{ value|currency }}

For example: Assuming value is `13`, `{{ value|currency }}` produces: `$13.00`

#### integer

Returns the given value as an int type.

Usage:

    {{ value|int }}
    {% tag_that_requires_int value|int %}

##### nolinebrs

Removes all `<br>` tags in the given string.

#### startswith

Returns whether the given value starts with the given string arg. The argument must be a string.

Usage:

    {{ value|startsvith:"arg" }}

#### creditcard

Hides parts of strings such as credit card or bank account numbers to show only the last amount of numbers. Default amount of numbers to show is **4**

Usage:

    {{ value|creditcard:chars_to_show }}

For example: Assuming value is `"5000000000003456"`

    {{ value|creditcard:4 }}

Produces:

    ************3456

#### verbose

Returns the verbose value of a ChoiceField.

Usage:

    {{ form.field|display }}

or

    {% for field in form %}
        {{ field|display }}
    {% endfor %}

For example: Assuming <field> is a BooleanField with True

    {{ field|display }}

Produces: The string `Yes`