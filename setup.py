import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

setup(
    name='django-template-utils',
    version='0.1',
    description='Just a collection of useful template tags and filters gathered in a single app.',
    long_description=README,
    author='Gerardo Orozco Mosqueda',
    author_email='gerardo.orozco.mosqueda@gmail.com',
    license='BSD',
    url='https://github.com/gerardo-orozco/django-template-utils',
    packages=['template_utils'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    install_requires=[
        'Django>=1.4',
    ]
)
