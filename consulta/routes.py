# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from flask import Blueprint, render_template, request, redirect, \
        flash, url_for
from .forms import ConsultaForm
from . import tryton
from . import app
from . import captcha
from .invoices import consultar_facturas, report

consulta = Blueprint('consulta', __name__, url_prefix='')
User = tryton.pool.get('res.user')

@tryton.default_context
def default_context():
    return User.get_preferences(context_only=True)

@consulta.route('/', methods = ['GET', 'POST'])
@tryton.transaction()
def index():
    form = ConsultaForm(request.form)

    if request.method == 'POST':
        #flash('Debido al incremento en los costos, nos vemos en la obligacion de realizar una adecuacion en los abonos de los servicios a partir de la facturacion de MAYO 2019.', 'info')
        if not form.validate():
            flash_errors(form)
        else:
            try:
                flash_msg = ''
                flash_type = 'error'
                app.logger.info('consultar_facturas: %s' % repr(request.form))
                (res_ok, result) = consultar_facturas(request.form)
                if res_ok:
                    nombre, invoices = result
                    return render_template('success.html', nombre=nombre, invoices=invoices)
                else:
                    flash_msg = result
                    flash(flash_msg, flash_type)
                    return render_template('consulta.html', form=form)
            except Exception as e:
                app.logger.error('No se realizo la consulta: %s' % repr(e))
                flash('There was a problem to procces.', 'error')

        return render_template('consulta.html', form=form)
    elif request.method == 'GET':
        form = ConsultaForm(request.form)
        return render_template('consulta.html', form=form)

@consulta.route('/comprobante/<record("account.invoice"):invoice>', methods = ['POST'])
@tryton.transaction()
def get_invoice(invoice):

    if request.method == 'POST':
        invoice_download = report(invoice)
        return invoice_download

def flash_errors(form):
    for field, errors in list(form.errors.items()):
        for error in errors:
            flash("Error en el campo %s - %s" % (
                getattr(form, field).label.text,
                error
            ), 'error')
