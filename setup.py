# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import os
import io
from configparser import ConfigParser
from setuptools import setup
from setuptools import find_packages


def read(fname):
    return io.open(
        os.path.join(os.path.dirname(__file__), fname),
        'r', encoding='utf-8').read()


def get_require_version(name):
    if minor_version % 2:
        require = '%s >= %s.%s.dev0, < %s.%s'
    else:
        require = '%s >= %s.%s, < %s.%s'
    require %= (name, major_version, minor_version,
        major_version, minor_version + 1)
    return require

config = ConfigParser()
config.read_file(open('tryton.cfg'))
info = dict(config.items('tryton'))
for key in ('depends', 'extras_depend', 'xml'):
    if key in info:
        info[key] = info[key].strip().splitlines()
version = info.get('version', '0.0.1')
major_version, minor_version, _ = version.split('.', 2)
major_version = int(major_version)
minor_version = int(minor_version)
name = 'tryton-consulta-facturas'

requires = []
requires.append(get_require_version('trytond'))
for dep in info.get('depends', []):
    requires.append(get_require_version('trytonar_%s' % dep))

requires.append('M2Crypto>=0.22.3')
requires.append('Pillow>=2.8.1')
requires.append('httplib2')
requires.append('pyafipws')
requires.append('pysimplesoap')
requires.append('Flask')
requires.append('Werkzeug<1.0')
requires.append('Jinja2<=2.10.3')
requires.append('Flask-Bootstrap')
requires.append('flask-tryton')
requires.append('flask-WTF')
requires.append('click>=5.1')

dependency_links = [
    'https://github.com/tryton-ar/party_ar/tarball/%s.%s#egg=trytonar_party_ar-%s.%s' \
        % (major_version, minor_version, major_version, minor_version),
    'https://github.com/tryton-ar/bank_ar/tarball/%s.%s#egg=trytonar_bank_ar-%s.%s' \
        % (major_version, minor_version, major_version, minor_version),
    'https://github.com/tryton-ar/account_ar/tarball/%s.%s#egg=trytonar_account_ar-%s.%s' \
        % (major_version, minor_version, major_version, minor_version),
    'https://github.com/tryton-ar/account_invoice_ar/tarball/%s.%s#egg=trytonar_account_invoice_ar-%s.%s' \
        % (major_version, minor_version, major_version, minor_version),
    'https://github.com/tryton-ar/payment_collect/tarball/%s.%s#egg=trytonar_payment_collect-%s.%s' \
        % (major_version, minor_version, major_version, minor_version),
    'https://gitlab.com/gcoop-libre/payment_collect_fastour/tree/%s.%s' % (
        major_version, minor_version),
    'https://github.com/reingart/pyafipws/tarball/py3k#egg=pyafipws',
    'https://github.com/pysimplesoap/pysimplesoap/tarball/stable_py3k#egg=pysimplesoap',
    ]

setup(name=name,
    version='0.1.0',
    author='gcoop',
    author_email='info@gcoop.coop',
    url='https://github.com/gcoop-libre/tryton-consulta-facturas',
    description='Invoices from Tryton Framework.',
    long_description=read('README'),
    py_modules=['tryton_consulta_facturas'],
    zip_safe=False,
    platforms='Posix; MacOS X; Windows',
    keywords='tryton flask',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    license='GPL-3',
    install_requires=requires,
    dependency_links=dependency_links,
    packages=find_packages("consulta"),
    package_dir={"": "consulta"},
    include_package_data=True,
    python_requires='>=3.4',
    )
