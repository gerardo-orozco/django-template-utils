# Contributing

Any helpful template tags and filters are very welcome.
Please feel free to help out :D

## Contributing with code

### Things to have in mind

- Please **always** bring to practcice PEPs
  [8](http://www.python.org/dev/peps/pep-0008/#code-lay-out),
  [20](http://www.python.org/dev/peps/pep-0020/) and
  [257](http://www.python.org/dev/peps/pep-0257/#specification) (at least)
- Please use descriptive commit messages.

### Adding new code

1. Fork and clone the project
2. Hack at will
3. Write appropriate tests
4. Write appropriate docstrings in the tags and filters code
5. Ensure all the tests pass
6. Give a breif explanation of the usage in README.md
7. Commit and push
8. Send a pull request

### Fixing stuff

1. Fork and clone the project
2. Fix the bugs you find in whichever way you consider it won't fail anymore
3. Ensure all the tests pass and that the documentation and usage
instructions still fit the changes; please fix any discrepancy
4. Commit and push
5. Send a pull request

## Reporting bugs

If you found a bug on any tag and/or filter and don't want to
or don't know how to fix it, no problem! Just open a
[new issue](https://github.com/gerardo-orozco/django-template-utils/issues/new):

1. Add a short, descriptive title for the bug you found
(i.e. *Error parsing values in "somefilter"*)
2. Add a description of what's the problem and the output of the error/bug
you found, or the unexpected behavior you got;whatever that fits your case.
**The more detailed this description, the better.**
3. Describe the steps needed to successfully reproduce the bug.
*Please include input data and any relevant information in these steps.*
4. Add the label `bug` to your issue.
5. Submit your new issue. I'll try to reply and fix it as soon as possible.

For steps 2 and 3, you may refer to this
[issue template](https://github.com/gerardo-orozco/django-template-utils/blob/master/ISSUE_TEMPLATE.md).