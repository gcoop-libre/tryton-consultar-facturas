#! -*- coding: utf8 -*-
# invoices.py
import ssl
import mimetypes
import io
from urllib.request import urlopen
from json import loads
from . import tryton
from . import app
from flask import send_file

Invoice = tryton.pool.get('account.invoice')
Lang = tryton.pool.get('ir.lang')
Party = tryton.pool.get('party.party')
PartyIdentifier = tryton.pool.get('party.identifier')

def consultar_facturas(data):
    "consultar_facturas"

    result = 'Los datos ingresados son incorrectos'
    res_ok = False
    cuit = data.get('identificador')
    nro_cliente = data.get('nro_cliente')
    identifiers = PartyIdentifier.search([
            ('type', '=', 'ar_cuit'),
            ('code', '=', cuit),
            ])
    invoices = Invoice.search([
            ('party.identifiers.code', '=', nro_cliente),
            ])
    if len(identifiers) > 0 and len(invoices) > 0:
        for identifier in identifiers:
            if identifier.party.id == invoices[0].party.id:
                result = [invoices[0].party.name, get_invoices(cuit, nro_cliente)]
                res_ok = True
                break

    return (res_ok, result)

def get_invoices(vat_number, client_number):
    "get invoices"
    #print request.remote_addr
    #print format(socket.gethostname())
    desde, hasta = ('', '')
    category = []
    filters = None
    offset = None
    limit = 13

    if filters is not None:
        for filtro in filters.split('|'):
            (value, query) = filtro.split('::')
            if value == 'date':
                (desde, hasta) = query.split(':')
            if value == 'category':
                category = query.split(',')

    query = [
        ('party.vat_number', '=', vat_number),
        ('type', '=', 'out'),
        ('state', 'in', ['posted', 'paid']),
        ('party.identifiers.code', '=', client_number),
    ]

    if desde != '':
        year = int(desde[:4])
        month = int(desde[4:6])
        start_date = date(year, month, 1)
        query.append(('invoice_date', '>=', start_date))
    if hasta != '':
        year = int(hasta[:4])
        month = int(hasta[4:6])
        end_date = date(year, month, monthrange(year, month)[1])
        query.append(('invoice_date', '<=', end_date))
    if category != []:
        query.append(('lines.product.template.category.name', 'in', category))
    #if client_number:
    #    query.append(['OR',
    #        ('client_number', '=', client_number),
    #        ('client_identifier.code', '=', client_number),
    #     ])

    invoices = Invoice.search(query, order=[('invoice_date', 'DESC')], limit=limit)

    data = []
    lang, = Lang.search([('code', '=', 'es')])
    digits = 2
    for invoice in invoices:
        currency_amount = Lang.currency(lang, invoice.total_amount,
            invoice.currency)
        number_amount = Lang.format(lang, '%.' + str(digits) + 'f',
            invoice.total_amount)
        data.append({
            "id": invoice.id,
            "invoice_type": invoice.invoice_type.invoice_type_string,
            "number": invoice.number,
            "invoice_date": invoice.invoice_date.strftime("%d/%m/%Y"),
            "total_amount": currency_amount,
            "number_amount": number_amount,
            "vat_number": vat_number,
            "state": invoice.state,
            "href": "/comprobante/"+str(invoice.id),
            "party_name": invoice.party.name,
        })

        if client_number:
            data[-1].update({"client_number": client_number})

    return data

def report(invoice):
    "get report"
    InvoiceReport = tryton.pool.get('account.invoice', type='report')
    type_, file_data, print_, name = InvoiceReport.execute([invoice.id], {})
    name = name.replace(' ', '').replace('-','_').lower()

    return send_file(io.BytesIO(file_data), attachment_filename=name,
        mimetype=mimetypes.types_map['.'+type_]  # pasar el mimetype
)
